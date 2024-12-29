"""FIX message validation"""

from typing import Any, List, Mapping, Tuple

from ..meta_data import (
    ProtocolMetaData,
    FieldMetaData
)

from .errors import FieldValueError
from .common import calc_checksum, calc_body_length
from .value_encoders import encode_value


def _assert_field_value_matches(
        field: FieldMetaData,
        expected: bytes,
        received: bytes
) -> None:
    if expected != received:
        raise FieldValueError(field, expected, received)


def assert_message_valid(
        protocol: ProtocolMetaData,
        buf: bytes,
        encoded_message: List[Tuple[bytes, bytes]],
        decoded_message: Mapping[str, Any],
        sep: bytes,
        convert_sep_to_soh_for_checksum: bool
) -> None:
    """Check the message is valid

    Args:
        protocol (ProtocolMetaData): The protocol meta data
        buf (bytes): The FIX message as bytes
        encoded_message (List[Tuple[bytes, bytes]]): The encoded message.
        decoded_message (Mapping[str, Any]): The decoded message
        sep (bytes): The field separator
        convert_sep_to_soh_for_checksum (bool): If true convert the separator
            before calculating the checksum.

    Raises:
        FieldValueError: If the message is invalid.
    """
    # Check the begin string.
    begin_string_field = protocol.fields_by_name['BeginString']
    begin_string_value = encode_value(
        protocol,
        begin_string_field,
        decoded_message[begin_string_field.name]
    )
    _assert_field_value_matches(
        begin_string_field,
        protocol.begin_string,
        begin_string_value
    )

    # Check the body length.
    body_length_field = protocol.fields_by_name['BodyLength']
    body_length_value = encode_value(
        protocol,
        body_length_field,
        decoded_message[body_length_field.name]
    )
    body_length = calc_body_length(buf, encoded_message, sep)
    _assert_field_value_matches(
        body_length_field,
        body_length_value,
        encode_value(protocol, body_length_field, body_length)
    )

    # Check the checksum.
    check_sum_field = protocol.fields_by_name['CheckSum']
    check_sum_value = encode_value(
        protocol,
        check_sum_field,
        decoded_message[check_sum_field.name]
    )
    check_sum = calc_checksum(buf, sep, convert_sep_to_soh_for_checksum)
    _assert_field_value_matches(
        check_sum_field,
        check_sum,
        check_sum_value
    )
