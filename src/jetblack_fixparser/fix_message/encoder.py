"""Encode a FIX message"""

from typing import Any, Iterator, List, Mapping, MutableMapping, Tuple, cast

from ..meta_data import (
    message_member_iter,
    MessageMemberMetaData,
    MessageMetaData,
    ProtocolMetaData
)
from ..meta_data.message_member import FieldMetaData

from .errors import EncodingError
from .common import SOH
from .value_encoders import encode_value


def _encode_fields(
        protocol: ProtocolMetaData,
        encoded_message: List[Tuple[bytes, bytes]],
        data: Mapping[str, Any],
        meta_data: Iterator[MessageMemberMetaData]
) -> None:
    for meta_datum in meta_data:
        # Check for required fields.
        if meta_datum.member.name not in data:
            if meta_datum.is_required:
                raise EncodingError(
                    f'required field "{meta_datum.member.name}" is missing'
                )
            continue

        item_data = data[meta_datum.member.name]
        if meta_datum.type == 'field':
            field_member = cast(FieldMetaData, meta_datum.member)
            value = encode_value(protocol, field_member, item_data)
            encoded_message.append((field_member.number, value))
        elif meta_datum.type == 'group':
            field_member = cast(FieldMetaData, meta_datum.member)
            item_list = cast(List[Mapping[str, Any]], item_data)
            value = encode_value(protocol, field_member, len(item_list))
            encoded_message.append((field_member.number, value))
            assert meta_datum.children is not None
            for group_item in item_list:
                _encode_fields(
                    protocol,
                    encoded_message,
                    group_item,
                    message_member_iter(meta_datum.children.values())
                )
        else:
            raise EncodingError(
                f'unknown type "{meta_datum.type}" for item "{meta_datum.member.name}"'
            )


def _regenerate_integrity(
        protocol: ProtocolMetaData,
        encoded_message: List[Tuple[bytes, bytes]],
        sep: bytes,
        convert_sep_for_checksum: bool
) -> Tuple[bytes, int, str]:
    body = sep.join(
        field + b'=' + value
        for field, value in encoded_message[2:-1]
    ) + sep
    body_length = len(body)

    encoded_header = [
        (protocol.fields_by_name['BeginString'].number, protocol.begin_string),
        (protocol.fields_by_name['BodyLength'].number,
         str(body_length).encode('ascii'))
    ]
    header = sep.join(
        field + b'=' + value
        for field, value in encoded_header
    ) + sep

    buf = header + body

    # Calculate the checksum
    checksum = sum(
        buf if sep == SOH or not convert_sep_for_checksum
        else buf.replace(sep, SOH)
    ) % 256
    checksum_str = f'{checksum:#03}'
    buf += protocol.fields_by_name['CheckSum'].number + \
        b'=' + checksum_str.encode('ascii') + sep

    return buf, body_length, checksum_str


def encode(
        protocol: ProtocolMetaData,
        data: MutableMapping[str, Any],
        meta_data: MessageMetaData,
        *,
        sep: bytes = SOH,
        regenerate_integrity: bool = True,
        convert_sep_for_checksum: bool = True
) -> bytes:
    """Encode a FIX message.

    Args:
        protocol (ProtocolMetaData): The FIX protocol.
        data (MutableMapping[str, Any]): The FIX message.
        meta_data (MessageMetaData): The message metadata.
        sep (bytes, optional): THe field separator. Defaults to SOH.
        regenerate_integrity (bool, optional): If true regenerate the message
            integrity, including the body length and checksum. Defaults to True.
        convert_sep_for_checksum (bool, optional): If true convert the field
            separator to SOH when calculating the checksum. Defaults to True.

    Returns:
        bytes: The encoded FIX message as a bytes buffer.
    """
    encoded_message: List[Tuple[bytes, bytes]] = []

    if regenerate_integrity:
        data['BeginString'] = protocol.begin_string.decode('ascii')
        data['BodyLength'] = 0
        data['CheckSum'] = '000'

    _encode_fields(
        protocol,
        encoded_message,
        data,
        message_member_iter(protocol.header.values())
    )
    _encode_fields(
        protocol,
        encoded_message,
        data,
        message_member_iter(meta_data.fields.values())
    )
    _encode_fields(
        protocol,
        encoded_message,
        data,
        message_member_iter(protocol.trailer.values())
    )

    if regenerate_integrity:
        buf, body_length, checksum = _regenerate_integrity(
            protocol,
            encoded_message,
            sep,
            convert_sep_for_checksum
        )
        data['BodyLength'] = body_length
        data['CheckSum'] = checksum
    else:
        buf = sep.join(
            field + b'=' + value
            for field, value in encoded_message
        ) + sep

    return buf
