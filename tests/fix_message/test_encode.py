"""Tests for encoding"""

from datetime import datetime, timezone

from jetblack_fixparser import load_yaml_protocol, FixMessage


def test_encode_logon():
    """Test encoding"""
    protocol = load_yaml_protocol(
        'etc/FIX44.yaml',
        is_millisecond_time=True,
        is_float_decimal=True,
        is_bool_enum=False
    )
    sending_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
    messages = [
        {
            'MsgType': 'LOGON',
            'MsgSeqNum': 42,
            'SenderCompID': "SENDER",
            'TargetCompID': "TARGET",
            'SendingTime': sending_time,
            'EncryptMethod': "NONE",
            'HeartBtInt': 30
        },
        {
            'MsgType': 'LOGOUT',
            'MsgSeqNum': 43,
            'SenderCompID': "SENDER",
            'TargetCompID': "TARGET",
            'SendingTime': sending_time
        },
        {
            'MsgType': 'HEARTBEAT',
            'MsgSeqNum': 43,
            'SenderCompID': "SENDER",
            'TargetCompID': "TARGET",
            'SendingTime': sending_time
        },
        {
            'MsgType': 'RESEND_REQUEST',
            'MsgSeqNum': 42,
            'SenderCompID': "SENDER",
            'TargetCompID': "TARGET",
            'SendingTime': sending_time,
            'BeginSeqNo': 10,
            'EndSeqNo': 12
        },
        {
            'MsgType': 'TEST_REQUEST',
            'MsgSeqNum': 42,
            'SenderCompID': "SENDER",
            'TargetCompID': "TARGET",
            'SendingTime': sending_time,
            'TestReqID': "This is not a test"
        },
        {
            'MsgType': 'SEQUENCE_RESET',
            'MsgSeqNum': 42,
            'SenderCompID': "SENDER",
            'TargetCompID': "TARGET",
            'SendingTime': sending_time,
            'GapFillFlag': False,
            'NewSeqNo': 12
        }
    ]
    for message in messages:
        fix_message = FixMessage(protocol, message)
        encoded_message = fix_message.encode(regenerate_integrity=True)
        roundtrip = FixMessage.decode(protocol, encoded_message)
        assert fix_message.message == roundtrip.message
