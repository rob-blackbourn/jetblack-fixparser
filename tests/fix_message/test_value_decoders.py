"""Tests for value decoders"""

import pytest

from jetblack_fixparser import load_yaml_protocol
from jetblack_fixparser.meta_data import ProtocolMetaData
from jetblack_fixparser.fix_message.value_decoders import (
    _decode_utc_timestamp,
    _decode_utc_time_only
)


@pytest.fixture
def protocol():
    return load_yaml_protocol(
        'etc/FIX44.yaml',
        is_millisecond_time=False,
        is_float_decimal=True
    )


def test_decode_utc_timestamp(protocol: ProtocolMetaData) -> None:
    """Tests for decoding UTC timestamps"""
    src = "20200312-15:35:13"
    dest = _decode_utc_timestamp(
        protocol,
        protocol.fields_by_name['SendingTime'],
        src.encode('ascii')
    )
    assert dest.strftime("%Y%m%d-%H:%M:%S") == src

    src = "20200312-15:35:13.123"
    dest = _decode_utc_timestamp(
        protocol,
        protocol.fields_by_name['SendingTime'],
        src.encode('ascii')
    )
    assert dest.strftime("%Y%m%d-%H:%M:%S.%f")[:-3] == src

    src = "20200312-15:35:13.123456"
    dest = _decode_utc_timestamp(
        protocol,
        protocol.fields_by_name['SendingTime'],
        src.encode('ascii')
    )
    assert dest.strftime("%Y%m%d-%H:%M:%S.%f") == src


def test_decode_utc_time_only(protocol: ProtocolMetaData) -> None:
    """Tests for decoding UTC times"""
    src = "15:35:13"
    dest = _decode_utc_time_only(
        protocol,
        protocol.fields_by_name['SendingTime'],
        src.encode('ascii')
    )
    assert dest.strftime("%H:%M:%S") == src

    src = "15:35:13.123"
    dest = _decode_utc_time_only(
        protocol,
        protocol.fields_by_name['SendingTime'],
        src.encode('ascii')
    )
    assert dest.strftime("%H:%M:%S.%f")[:-3] == src

    src = "15:35:13.123456"
    dest = _decode_utc_time_only(
        protocol,
        protocol.fields_by_name['SendingTime'],
        src.encode('ascii')
    )
    assert dest.strftime("%H:%M:%S.%f") == src
