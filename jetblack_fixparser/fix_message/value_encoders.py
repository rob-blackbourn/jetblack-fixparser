"""Value Encoders"""

from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, List, Mapping, Union

from ..meta_data import ProtocolMetaData, FieldMetaData
from ..types import ValueType

from .common import(
    UTCTIMESTAMP_FMT_NO_MILLIS,
    UTCTIMESTAMP_FMT_MILLIS,
    UTCTIMEONLY_FMT_NO_MILLIS,
    UTCTIMEONLY_FMT_MILLIS,
    is_encodeable_enum
)
from .errors import EncodingError


def _encode_int(
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: Union[int, str]
) -> bytes:
    if is_encodeable_enum(protocol, meta_data, value, ValueType.INT):
        return meta_data.values_by_name[value]  # type: ignore
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
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: str
) -> bytes:
    if is_encodeable_enum(protocol, meta_data, value, ValueType.CHAR):
        return meta_data.values_by_name[value]  # type: ignore
    else:
        return value.encode()


def _encode_string(
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: str
) -> bytes:
    if is_encodeable_enum(protocol, meta_data, value, ValueType.STRING):
        return meta_data.values_by_name[value]  # type: ignore
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
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: Union[bool, str]
) -> bytes:
    if is_encodeable_enum(protocol, meta_data, value, ValueType.BOOLEAN):
        return meta_data.values_by_name[value]  # type: ignore
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


Encoder = Callable[[ProtocolMetaData, FieldMetaData, Any], bytes]

_ENCODERS: Mapping[str, Encoder] = {
    ValueType.INT.name: _encode_int,
    ValueType.SEQNUM.name: _encode_seqnum,
    ValueType.NUMINGROUP.name: _encode_numingroup,
    ValueType.LENGTH.name: _encode_length,
    ValueType.FLOAT.name: _encode_float,
    ValueType.QTY.name: _encode_qty,
    ValueType.PRICE.name: _encode_price,
    ValueType.PRICEOFFSET.name: _encode_price_offset,
    ValueType.AMT.name: _encode_amt,
    ValueType.CHAR.name: _encode_char,
    ValueType.STRING.name: _encode_string,
    ValueType.CURRENCY.name: _encode_currency,
    ValueType.EXCHANGE.name: _encode_exchange,
    ValueType.BOOLEAN.name: _encode_bool,
    ValueType.MULTIPLEVALUESTRING.name: _encode_multi_value_str,
    ValueType.UTCTIMESTAMP.name: _encode_utc_timestamp,
    ValueType.UTCTIMEONLY.name: _encode_utc_time_only,
    ValueType.LOCALMKTDATE.name: _encode_localmktdate,
    ValueType.UTCDATE.name: _encode_utcdate,
    ValueType.MONTHYEAR.name: _encode_monthyear
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
