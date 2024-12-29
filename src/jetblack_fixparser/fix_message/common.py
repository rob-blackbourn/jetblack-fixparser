"""Common Code"""

from typing import Any, List, Tuple, Union

from ..meta_data import ProtocolMetaData, FieldMetaData
from ..types import ValueType


SOH = b'\x01'

UTCTIMESTAMP_FMT_MILLIS = '%Y%m%d-%H:%M:%S.%f'
UTCTIMESTAMP_FMT_NO_MILLIS = '%Y%m%d-%H:%M:%S'
UTCTIMEONLY_FMT_MILLIS = '%H:%M:%S.%f'
UTCTIMEONLY_FMT_NO_MILLIS = '%H:%M:%S'


def calc_checksum(
        buf: bytes,
        sep: bytes = SOH,
        convert_sep_to_soh_for_checksum: bool = False
) -> bytes:
    """Calculate the FIX message checksum.

    In production the separator is always SOH (ascii 0x01). For diagnostics the
    '|' charactor is often used to allow the message to be printed. As this will
    give a different checksum a flag is provided to convert the separator to SOH
    if required.

    Args:
        buf (bytes): The FIX message buffer.
        sep (bytes, optional): The separator. Defaults to SOH.
        convert_sep_to_soh_for_checksum (bool, optional): If true convert the
            separator to SOH before calculating the checksum. Defaults to False.

    Returns:
        bytes: The checksum.
    """
    if sep != SOH and convert_sep_to_soh_for_checksum:
        buf = buf.replace(sep, SOH)

    check_sum = sum(buf[:-len(b'10=000\x01')]) % 256
    return f'{check_sum:#03}'.encode('ascii')


def calc_body_length(
        buf: bytes,
        encoded_message: List[Tuple[bytes, bytes]],
        sep: bytes = SOH
) -> int:
    """Calculate the body length

    Args:
        buf (bytes): The FIX message buffer
        encoded_message (List[Tuple[bytes, bytes]]): The encoded FIX message
        sep (bytes, optional): The message separator. Defaults to SOH.

    Returns:
        int: The length of the body.
    """
    header = sep.join([
        b'='.join(field_value)
        for field_value in encoded_message[:2]
    ]) + sep
    trailer = b'='.join(encoded_message[-1]) + sep
    body_length = len(buf) - len(header) - len(trailer)
    return body_length


def is_decodeable_enum(
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: bytes,
        value_type: ValueType
):
    return (
        protocol.is_type_enum.get(value_type, True) and
        meta_data.values and
        value in meta_data.values
    )


def is_encodeable_enum(
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: Union[Any, str],
        value_type: ValueType
) -> bool:
    return (
        isinstance(value, str) and
        meta_data.values_by_name and
        value in meta_data.values_by_name and
        protocol.is_type_enum.get(value_type, True)
    )
