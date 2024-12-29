"""Fix message decoder"""

from typing import (
    Any,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Set,
    Tuple,
    cast
)

from ..meta_data import (
    ProtocolMetaData,
    FieldMetaData,
    MessageMemberMetaData,
    message_member_iter,
    MessageMetaData
)

from .errors import DecodingError
from .common import SOH
from .validation import assert_message_valid
from .value_decoders import decode_value
from .value_encoders import encode_value


def _split_item(item: bytes) -> Tuple[bytes, bytes]:
    field_id, _, field_value = item.partition(b'=')
    return field_id, field_value


def _to_encoded_message(buf: bytes, sep: bytes) -> List[Tuple[bytes, bytes]]:
    encoded_message: List[Tuple[bytes, bytes]] = [
        _split_item(field_value)
        for field_value in buf.split(sep)
    ]
    return encoded_message[:-1]


def _find_next_member(
        received_field: FieldMetaData,
        meta_data: Iterator[MessageMemberMetaData],
        strict: bool
) -> Optional[MessageMemberMetaData]:
    # Find the next matching field.
    while True:
        try:
            meta_datum = next(meta_data)
            # TODO: Always field?
            field = cast(FieldMetaData, meta_datum.member)
            if field.number == received_field.number:
                return meta_datum

            if meta_datum.is_required and strict:
                raise DecodingError(
                    f'required field missing {meta_datum.member.name}'
                )

        except StopIteration:
            return None


def _decode_fields_in_order(
        protocol: ProtocolMetaData,
        encoded_message: List[Tuple[bytes, bytes]],
        index: int,
        meta_data: Iterator[MessageMemberMetaData],
        decoded_message: MutableMapping[str, Any],
        strict: bool
) -> int:
    while index < len(encoded_message):

        field_number, value = encoded_message[index]
        received_field = protocol.fields_by_number.get(field_number)
        if not received_field:
            raise DecodingError(
                f'received unknown field "{field_number!r}" of value "{value!r}"'
            )
        meta_datum = _find_next_member(received_field, meta_data, strict)
        if not meta_datum:
            break
        index += 1

        if meta_datum.type == 'group':
            _, index = _decode_group(
                protocol,
                encoded_message,
                index,
                meta_datum,
                int(value),
                strict
            )
            decoded_message[received_field.name] = value
        else:
            decoded_message[received_field.name] = decode_value(
                protocol,
                received_field,
                value
            )

    # Check if any members are required.
    required_fields = [
        meta_datum.member.name
        for meta_datum in meta_data
        if meta_datum.is_required
    ]
    if len(required_fields) > 0:
        raise DecodingError(f'required fields missing: {required_fields}')

    return index


def _decode_fields_any_order(
        protocol: ProtocolMetaData,
        encoded_message: List[Tuple[bytes, bytes]],
        index: int,
        meta_data: MutableMapping[bytes, MessageMemberMetaData],
        decoded_message: MutableMapping[str, Any],
        strict: bool = True
) -> int:
    field_names_found: Set[str] = set()
    while index < len(encoded_message):

        field_number, value = encoded_message[index]
        received_field = protocol.fields_by_number[field_number]
        meta_datum = meta_data.get(field_number)
        if not meta_datum:
            break

        field_names_found.add(received_field.name)
        index += 1

        if meta_datum.type == 'group':
            decoded_groups, index = _decode_group(
                protocol,
                encoded_message,
                index,
                meta_datum,
                int(value),
                strict
            )
            decoded_message[received_field.name] = decoded_groups
        else:
            decoded_message[received_field.name] = decode_value(
                protocol,
                received_field,
                value
            )

    required_members = [
        meta_datum.member.name
        for meta_datum in meta_data.values()
        if meta_datum.is_required and meta_datum.member.name not in field_names_found
    ]
    if len(required_members) > 0:
        raise DecodingError(f'required fields missing: {required_members}')

    return index


def _decode_group(
        protocol: ProtocolMetaData,
        encoded_message: List[Tuple[bytes, bytes]],
        index: int,
        meta_data: MessageMemberMetaData,
        count: int,
        strict: bool
) -> Tuple[List[MutableMapping[str, Any]], int]:
    assert meta_data.children is not None
    decoded_groups: List[MutableMapping[str, Any]] = []
    for _ in range(int(count)):
        decoded_group: MutableMapping[str, Any] = {}
        index = _decode_fields_in_order(
            protocol,
            encoded_message,
            index,
            message_member_iter(meta_data.children.values()),
            decoded_group,
            strict
        )
        decoded_groups.append(decoded_group)
    return decoded_groups, index


def _decode_header(
        protocol: ProtocolMetaData,
        encoded_message: List[Tuple[bytes, bytes]],
        decoded_message: MutableMapping[str, Any],
        strict: bool
) -> int:
    # The first three header fields must be in order.
    header_fields = list(message_member_iter(protocol.header.values()))
    index = _decode_fields_in_order(
        protocol,
        encoded_message,
        0,
        iter(header_fields[:3]),
        decoded_message,
        strict
    )

    # The rest can be in any order.
    index = _decode_fields_any_order(
        protocol,
        encoded_message,
        index,
        {
            cast(FieldMetaData, message_member.member).number: message_member
            for message_member in header_fields[3:]
        },
        decoded_message,
        strict
    )

    return index


def _decode_body(
        protocol: ProtocolMetaData,
        encoded_message: List[Tuple[bytes, bytes]],
        index: int,
        meta_data: MessageMetaData,
        decoded_message: MutableMapping[str, Any],
        strict: bool
) -> int:
    # Body fields can be in any order
    index = _decode_fields_any_order(
        protocol,
        encoded_message,
        index,
        {
            cast(FieldMetaData, message_member.member).number: message_member
            for message_member in message_member_iter(meta_data.fields.values())
        },
        decoded_message,
        strict
    )

    return index


def _decode_trailer(
        protocol: ProtocolMetaData,
        encoded_message: List[Tuple[bytes, bytes]],
        index: int,
        decoded_message: MutableMapping[str, Any],
        strict: bool
) -> int:
    # All but the last field can be in any order.
    trailer_fields = list(message_member_iter(protocol.trailer.values()))
    index = _decode_fields_any_order(
        protocol,
        encoded_message,
        index,
        {
            cast(FieldMetaData, message_member.member).number: message_member
            for message_member in trailer_fields[:-1]
        },
        decoded_message,
        strict
    )

    # The last field should be the checksum.
    index = _decode_fields_in_order(
        protocol,
        encoded_message,
        index,
        iter(trailer_fields[-1:]),
        decoded_message,
        strict
    )

    return index


def find_message_meta_data(
        protocol: ProtocolMetaData,
        message: Mapping[str, Any]
) -> MessageMetaData:
    """Find the meta data for the message

    Args:
        protocol (ProtocolMetaData): The protocol meta data
        message (Mapping[str, Any]): The FIX message

    Returns:
        MessageMetaData: The message meta data.
    """
    msgtype_field = protocol.fields_by_name['MsgType']
    msgtype = encode_value(
        protocol,
        msgtype_field,
        message[msgtype_field.name]
    )
    meta_data = protocol.messages_by_type[msgtype]
    return meta_data


def decode(
        protocol: ProtocolMetaData,
        buf: bytes,
        *,
        strict: bool = True,
        validate: bool = True,
        sep: bytes = SOH,
        convert_sep_for_checksum: bool = True
) -> Tuple[MutableMapping[str, Any], MessageMetaData]:
    """Decode a FIX bytes buffer

    Args:
        protocol (ProtocolMetaData): The protocol meta data.
        buf (bytes): The FIX bytes buffer.
        strict (bool, optional): If true use strict validation. Defaults to True.
        validate (bool, optional): If true validate the message. Defaults to
            True.
        sep (bytes, optional): The field separator. Defaults to SOH.
        convert_sep_for_checksum (bool, optional): If true convert the separator
            before calculating the checksum. Defaults to True.

    Returns:
        Tuple[MutableMapping[str, Any], MessageMetaData]: The message and it's
            meta data
    """
    encoded_message = _to_encoded_message(buf, sep)
    decoded_message: MutableMapping[str, Any] = {}

    index = _decode_header(
        protocol,
        encoded_message,
        decoded_message,
        strict
    )
    meta_data = find_message_meta_data(protocol, decoded_message)

    index = _decode_body(
        protocol,
        encoded_message,
        index,
        meta_data,
        decoded_message,
        strict
    )

    _decode_trailer(
        protocol,
        encoded_message,
        index,
        decoded_message,
        strict
    )

    if validate:
        assert_message_valid(
            protocol,
            buf,
            encoded_message,
            decoded_message,
            sep,
            convert_sep_for_checksum
        )

    return decoded_message, meta_data
