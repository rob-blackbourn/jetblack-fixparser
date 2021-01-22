"""Test the loader"""

from jetblack_fixparser import load_yaml_protocol, ValueType


def test_loader():
    """Test the loader"""
    assert load_yaml_protocol('etc/FIX40.yaml') is not None
    assert load_yaml_protocol('etc/FIX41.yaml') is not None
    assert load_yaml_protocol('etc/FIX42.yaml') is not None
    assert load_yaml_protocol('etc/FIX43.yaml') is not None
    assert load_yaml_protocol('etc/FIX44.yaml') is not None


def test_loader_is_type_enum():
    """Tests for is_type_enum"""
    assert load_yaml_protocol(
        'etc/FIX44.yaml',
        is_type_enum={ValueType.BOOLEAN: False}
    ) is not None
    assert load_yaml_protocol(
        'etc/FIX44.yaml',
        is_type_enum={'BOOLEAN': False}
    ) is not None
