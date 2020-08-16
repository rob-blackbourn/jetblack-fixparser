"""Value Decoders"""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, List, Union

from ..meta_data import ProtocolMetaData, FieldMetaData
from .errors import DecodingError

from .common import (
    UTCTIMEONLY_FMT_MILLIS,
    UTCTIMEONLY_FMT_NO_MILLIS,
    UTCTIMESTAMP_FMT_MILLIS,
    UTCTIMESTAMP_FMT_NO_MILLIS
)


def _decode_int(
        _protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: bytes
) -> Union[int, str]:
    if meta_data.values and value in meta_data.values:
        return meta_data.values[value]
    else:
        return int(value.lstrip(b'0') or b'0')


def _decode_seqnum(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> int:
    return int(value.lstrip(b'0') or b'0')


def _decode_numingroup(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> int:
    return int(value.lstrip(b'0') or b'0')


def _decode_length(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> int:
    return int(value.lstrip(b'0') or b'0')


def _decode_float(
        protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> Union[float, Decimal]:
    return Decimal(value.decode('ascii')) if protocol.is_float_decimal else float(value)


def _decode_qty(
        protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> Union[float, Decimal]:
    return Decimal(value.decode('ascii')) if protocol.is_float_decimal else float(value)


def _decode_price(
        protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> Union[float, Decimal]:
    return Decimal(value.decode('ascii')) if protocol.is_float_decimal else float(value)


def _decode_price_offset(
        protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> Union[float, Decimal]:
    return Decimal(value.decode('ascii')) if protocol.is_float_decimal else float(value)


def _decode_amt(
        protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> Union[float, Decimal]:
    return Decimal(value.decode('ascii')) if protocol.is_float_decimal else float(value)


def _decode_char(
        _protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: bytes
) -> str:
    if meta_data.values and value in meta_data.values:
        return meta_data.values[value]
    else:
        return value.decode('ascii')


def _decode_string(
        _protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: bytes
) -> str:
    if meta_data.values and value in meta_data.values:
        return meta_data.values[value]
    else:
        return value.decode('ascii')


def _decode_currency(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> str:
    return value.decode('ascii')


def _decode_exchange(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> str:
    return value.decode('ascii')


def _decode_multiple_value_str(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> List[str]:
    return value.decode('ascii').split(' ')


def _decode_bool(
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: bytes
) -> Union[bool, str]:
    if protocol.is_bool_enum and meta_data.values and value in meta_data.values:
        return meta_data.values[value]
    else:
        return value == b'Y'


def _decode_utc_timestamp(
        protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> datetime:
    if protocol.is_millisecond_time:
        return datetime.strptime(
            value.decode('ascii'),
            UTCTIMESTAMP_FMT_MILLIS
        ).replace(tzinfo=timezone.utc)
    else:
        return datetime.strptime(
            value.decode('ascii'),
            UTCTIMESTAMP_FMT_NO_MILLIS
        ).replace(tzinfo=timezone.utc)


def _decode_utc_time_only(
        protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> datetime:
    if protocol.is_millisecond_time:
        return datetime.strptime(value.decode('ascii'), UTCTIMEONLY_FMT_MILLIS)
    else:
        return datetime.strptime(value.decode('ascii'), UTCTIMEONLY_FMT_NO_MILLIS)


def _decode_localmktdate(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> datetime:
    return datetime.strptime(value.decode('ascii'), '%Y%m%d')


def _decode_utcdate(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> datetime:
    return datetime.strptime(value.decode('ascii'), '%Y%m%d')


def _decode_monthyear(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: bytes
) -> str:
    return value.decode('ascii')


_DECODERS = {
    'INT': _decode_int,
    'SEQNUM': _decode_seqnum,
    'NUMINGROUP': _decode_numingroup,
    'LENGTH': _decode_length,
    'FLOAT': _decode_float,
    'QTY': _decode_qty,
    'PRICE': _decode_price,
    'PRICEOFFSET': _decode_price_offset,
    'AMT': _decode_amt,
    'CHAR': _decode_char,
    'STRING': _decode_string,
    'CURRENCY': _decode_currency,
    'EXCHANGE': _decode_exchange,
    'BOOLEAN': _decode_bool,
    'MULTIPLEVALUESTRING': _decode_multiple_value_str,
    'UTCTIMESTAMP': _decode_utc_timestamp,
    'UTCTIMEONLY': _decode_utc_time_only,
    'LOCALMKTDATE': _decode_localmktdate,
    'UTCDATE': _decode_utcdate,
    'MONTHYEAR': _decode_monthyear
}


def decode_value(
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: bytes
) -> Any:
    """Decoide the value of a field

    Args:
        protocol (ProtocolMetaData): The FIX protocol
        meta_data (FieldMetaData): The field meta data
        value (bytes): The value of the field

    Returns:
        Any: [description]
    """

    if not value:
        return None

    decoder = _DECODERS.get(meta_data.type)
    if not decoder:
        raise DecodingError(f'Unknown type "{meta_data.type}"')
    return decoder(protocol, meta_data, value)
