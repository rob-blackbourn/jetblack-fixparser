"""Test the loader"""

from jetblack_fixparser.loader import load_yaml_protocol


def test_loader():
    """Test the loader"""
    assert load_yaml_protocol('etc/FIX40.yaml') is not None
    assert load_yaml_protocol('etc/FIX41.yaml') is not None
    assert load_yaml_protocol('etc/FIX42.yaml') is not None
    assert load_yaml_protocol('etc/FIX43.yaml') is not None
    assert load_yaml_protocol('etc/FIX44.yaml') is not None
