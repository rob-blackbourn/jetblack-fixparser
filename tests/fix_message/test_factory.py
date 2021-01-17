"""Tests for factory encoding"""

from datetime import datetime, timezone

from jetblack_fixparser import (
    load_yaml_protocol,
    FixMessage,
    FixMessageFactory,
    ValueType
)


def test_fix_message_factory():
    """Test the message factory"""
    protocol = load_yaml_protocol(
        'etc/FIX44.yaml',
        is_millisecond_time=True,
        is_float_decimal=True,
        is_type_enum={ValueType.BOOLEAN: False}
    )
    factory = FixMessageFactory(protocol, "SENDER", "TARGET")
    sending_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
    fix_messages = [
        factory.create(
            'LOGON',
            42,
            sending_time,
            {
                'EncryptMethod': "NONE",
                'HeartBtInt': 30
            }
        ),
        factory.create(
            'LOGOUT',
            42,
            sending_time,
            {
            }
        ),
        factory.create(
            'HEARTBEAT',
            43,
            sending_time,
            {
            }
        ),
        factory.create(
            'RESEND_REQUEST',
            44,
            sending_time,
            {
                'BeginSeqNo': 10,
                'EndSeqNo': 12
            }
        ),
        factory.create(
            'TEST_REQUEST',
            45,
            sending_time,
            {
                'TestReqID': "This is not a test"
            }
        ),
        factory.create(
            'SEQUENCE_RESET',
            46,
            sending_time,
            {
                'GapFillFlag': False,
                'NewSeqNo': 12
            }
        )
    ]
    for fix_message in fix_messages:
        encoded_message = fix_message.encode(regenerate_integrity=True)
        roundtrip = FixMessage.decode(protocol, encoded_message)
        assert fix_message.message == roundtrip.message
