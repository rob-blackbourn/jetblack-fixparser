"""Tests for fIX 4.2"""

import pytest

from jetblack_fixparser import load_yaml_protocol, FixMessage


@pytest.fixture
def protocol_42():
    return load_yaml_protocol(
        'etc/FIX42.yaml',
        is_millisecond_time=False,
        is_float_decimal=True
    )


@pytest.fixture
def protocol_42_millis():
    return load_yaml_protocol(
        'etc/FIX42.yaml',
        is_millisecond_time=True,
        is_float_decimal=True
    )


def test_new_order_single(protocol_42):
    """Test for New Single Order - BUY 100 CVS MKT DAY"""
    buf = b'8=FIX.4.2|9=146|35=D|49=ABC_DEFG01|56=CCG|115=XYZ|34=4|52=20090323-15:40:29|11=NF 0542/03232009|21=1|55=CVS|207=N|54=1|60=20090323-15:40:29|38=100|40=1|59=0|47=A|10=195|'
    msg = FixMessage.decode(
        protocol_42,
        buf,
        sep=b'|',
        strict=True,
        validate=True,
        convert_sep_for_checksum=True
    )
    round_trip = msg.encode(
        sep=b'|',
        regenerate_integrity=True,
        convert_sep_for_checksum=True
    )
    assert buf == round_trip


def test_order_acknowledgement(protocol_42):
    """Test for an Order Acknowledgement"""
    buf = b'8=FIX.4.2|9=227|35=8|49=CCG|56=ABC_DEFG01|128=XYZ|34=4|52=20090323-15:40:35|37=NF 0542/03232009|11=NF 0542/03232009|17=0|20=0|150=0|39=0|55=CVS|207=N|54=1|38=100|40=1|59=0|47=A|32=0|31=0|30=N|151=100|14=0|6=0|60=20090323-15:40:30|58=New order|10=205|'
    msg = FixMessage.decode(
        protocol_42,
        buf,
        sep=b'|',
        strict=True,
        validate=True,
        convert_sep_for_checksum=True
    )
    round_trip = msg.encode(
        sep=b'|',
        regenerate_integrity=True,
        convert_sep_for_checksum=True
    )
    assert buf == round_trip


def test_market_data(protocol_42_millis):
    """Market Data (incremental refresh)"""
    buf = b'8=FIX.4.2|9=196|35=X|49=A|56=B|34=12|52=20100318-03:21:11.364|262=A|268=2|279=0|269=0|278=BID|55=EUR/USD|270=1.37215|15=EUR|271=2500000|346=1|279=0|269=1|278=OFFER|55=EUR/USD|270=1.37224|15=EUR|271=2503200|346=1|10=171|'
    msg = FixMessage.decode(
        protocol_42_millis,
        buf,
        sep=b'|',
        strict=True,
        validate=True,
        convert_sep_for_checksum=True
    )
    round_trip = msg.encode(
        sep=b'|',
        regenerate_integrity=True,
        convert_sep_for_checksum=True
    )
    assert buf == round_trip


def test_indication_of_interest(protocol_42):
    """Indication of interest"""
    buf = b'8=FIX.4.2|9=97|35=6|49=BKR|56=IM|34=14|52=20100204-09:18:42|23=115685|28=N|55=SPMI.MI|54=2|27=S|44=2200.75|25=H|10=248|'
    msg = FixMessage.decode(
        protocol_42,
        buf,
        sep=b'|',
        strict=True,
        validate=True,
        convert_sep_for_checksum=True
    )
    round_trip = msg.encode(
        sep=b'|',
        regenerate_integrity=True,
        convert_sep_for_checksum=True
    )
    assert buf == round_trip
