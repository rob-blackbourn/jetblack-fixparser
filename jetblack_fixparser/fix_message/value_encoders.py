"""Value Encoders"""

from datetime import datetime
from decimal import Decimal
from typing import Any, List, Union

from ..meta_data import ProtocolMetaData, FieldMetaData

from .common import(
    UTCTIMESTAMP_FMT_NO_MILLIS,
    UTCTIMESTAMP_FMT_MILLIS,
    UTCTIMEONLY_FMT_NO_MILLIS,
    UTCTIMEONLY_FMT_MILLIS
)
from .errors import EncodingError


def _encode_int(
        _protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: Union[int, str]
) -> bytes:
    if isinstance(value, str) and meta_data.values_by_name and value in meta_data.values_by_name:
        return meta_data.values_by_name[value]
    else:
        return str(value).encode()


def _encode_seqnum(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: int
) -> bytes:
    return str(value).encode()


def _encode_numingroup(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: int
) -> bytes:
    return str(value).encode()


def _encode_length(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: int
) -> bytes:
    return str(value).encode()


def _encode_float(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: Union[Decimal, float, int]
) -> bytes:
    if isinstance(value, Decimal):
        return str(value).encode()
    elif value != int(value):
        return str(int(value)).encode()
    else:
        return str(value).encode()


def _encode_qty(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: Union[Decimal, float, int]
) -> bytes:
    if isinstance(value, Decimal):
        return str(value).encode()
    elif value != int(value):
        return str(int(value)).encode()
    else:
        return str(value).encode()


def _encode_price(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: Union[Decimal, float, int]
) -> bytes:
    if isinstance(value, Decimal):
        return str(value).encode()
    elif value != int(value):
        return str(int(value)).encode()
    else:
        return str(value).encode()


def _encode_price_offset(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: Union[Decimal, float, int]
) -> bytes:
    if isinstance(value, Decimal):
        return str(value).encode()
    elif value != int(value):
        return str(int(value)).encode()
    else:
        return str(value).encode()


def _encode_amt(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: Union[Decimal, float, int]
) -> bytes:
    if isinstance(value, Decimal):
        return str(value).encode()
    elif value != int(value):
        return str(int(value)).encode()
    else:
        return str(value).encode()


def _encode_char(
        _protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: str
) -> bytes:
    if meta_data.values_by_name and value in meta_data.values_by_name:
        return meta_data.values_by_name[value]
    else:
        return value.encode()


def _encode_string(
        _protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: str
) -> bytes:
    if meta_data.values_by_name and value in meta_data.values_by_name:
        return meta_data.values_by_name[value]
    else:
        return value.encode()


def _encode_currency(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: str
) -> bytes:
    return value.encode()


def _encode_exchange(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: str
) -> bytes:
    return value.encode()


def _encode_monthyear(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: str
) -> bytes:
    return value.encode()


def _encode_bool(
        _protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: Union[bool, str]
) -> bytes:
    if isinstance(value, str) and meta_data.values_by_name and value in meta_data.values_by_name:
        return meta_data.values_by_name[value]
    else:
        return b'Y' if value else b'N'


def _encode_multi_value_str(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: List[str]
) -> bytes:
    return ' '.join(value).encode()


def _encode_utc_timestamp(
        protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: datetime
) -> bytes:
    if protocol.is_millisecond_time:
        return value.strftime(UTCTIMESTAMP_FMT_MILLIS)[:-3].encode()
    else:
        return value.strftime(UTCTIMESTAMP_FMT_NO_MILLIS).encode()


def _encode_utc_time_only(
        protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: datetime
) -> bytes:
    if protocol.is_millisecond_time:
        return value.strftime(UTCTIMEONLY_FMT_MILLIS).encode()
    else:
        return value.strftime(UTCTIMEONLY_FMT_NO_MILLIS).encode()


def _encode_localmktdate(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: datetime
) -> bytes:
    return value.strftime('%Y%m%d').encode()


def _encode_utcdate(
        _protocol: ProtocolMetaData,
        _meta_data: FieldMetaData,
        value: datetime
) -> bytes:
    return value.strftime('%Y%m%d').encode()


_ENCODERS = {
    'INT': _encode_int,
    'SEQNUM': _encode_seqnum,
    'NUMINGROUP': _encode_numingroup,
    'LENGTH': _encode_length,
    'FLOAT': _encode_float,
    'QTY': _encode_qty,
    'PRICE': _encode_price,
    'PRICEOFFSET': _encode_price_offset,
    'AMT': _encode_amt,
    'CHAR': _encode_char,
    'STRING': _encode_string,
    'CURRENCY': _encode_currency,
    'EXCHANGE': _encode_exchange,
    'BOOLEAN': _encode_bool,
    'MULTIPLEVALUESTRING': _encode_multi_value_str,
    'UTCTIMESTAMP': _encode_utc_timestamp,
    'UTCTIMEONLY': _encode_utc_time_only,
    'LOCALMKTDATE': _encode_localmktdate,
    'UTCDATE': _encode_utcdate,
    'MONTHYEAR': _encode_monthyear
}


def encode_value(
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: Any
) -> bytes:
    """Encode a field value

    Args:
        protocol (ProtocolMetaData): The FIX protocol meta data
        meta_data (FieldMetaData): The field meta data
        value (Any): The value to encode

    Returns:
        bytes: The encoded field value
    """

    if value is None:
        return b''

    encoder = _ENCODERS.get(meta_data.type)
    if not encoder:
        raise EncodingError(f'Unknown type "{meta_data.type}"')

    return encoder(protocol, meta_data, value)
