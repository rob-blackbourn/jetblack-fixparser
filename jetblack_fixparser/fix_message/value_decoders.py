"""Value Decoders"""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Callable, List, Mapping, Union

from ..meta_data import ProtocolMetaData, FieldMetaData
from ..types import ValueType

from .common import is_decodeable_enum
from .errors import DecodingError

from .common import (
    UTCTIMEONLY_FMT_MILLIS,
    UTCTIMEONLY_FMT_NO_MILLIS,
    UTCTIMESTAMP_FMT_MILLIS,
    UTCTIMESTAMP_FMT_NO_MILLIS
)


def _decode_int(
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: bytes
) -> Union[int, str]:
    if is_decodeable_enum(protocol, meta_data, value, ValueType.INT):
        return meta_data.values[value]  # type: ignore
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
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: bytes
) -> str:
    if is_decodeable_enum(protocol, meta_data, value, ValueType.CHAR):
        return meta_data.values[value]  # type: ignore
    else:
        return value.decode('ascii')


def _decode_string(
        protocol: ProtocolMetaData,
        meta_data: FieldMetaData,
        value: bytes
) -> str:
    if is_decodeable_enum(protocol, meta_data, value, ValueType.STRING):
        return meta_data.values[value]  # type: ignore
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
    if is_decodeable_enum(protocol, meta_data, value, ValueType.BOOLEAN):
        return meta_data.values[value]  # type: ignore
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


Decoder = Callable[[ProtocolMetaData, FieldMetaData, bytes], Any]

_DECODERS: Mapping[str, Decoder] = {
    ValueType.INT.name: _decode_int,
    ValueType.SEQNUM.name: _decode_seqnum,
    ValueType.NUMINGROUP.name: _decode_numingroup,
    ValueType.LENGTH.name: _decode_length,
    ValueType.FLOAT.name: _decode_float,
    ValueType.QTY.name: _decode_qty,
    ValueType.PRICE.name: _decode_price,
    ValueType.PRICEOFFSET.name: _decode_price_offset,
    ValueType.AMT.name: _decode_amt,
    ValueType.CHAR.name: _decode_char,
    ValueType.STRING.name: _decode_string,
    ValueType.CURRENCY.name: _decode_currency,
    ValueType.EXCHANGE.name: _decode_exchange,
    ValueType.BOOLEAN.name: _decode_bool,
    ValueType.MULTIPLEVALUESTRING.name: _decode_multiple_value_str,
    ValueType.UTCTIMESTAMP.name: _decode_utc_timestamp,
    ValueType.UTCTIMEONLY.name: _decode_utc_time_only,
    ValueType.LOCALMKTDATE.name: _decode_localmktdate,
    ValueType.UTCDATE.name: _decode_utcdate,
    ValueType.MONTHYEAR.name: _decode_monthyear
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
