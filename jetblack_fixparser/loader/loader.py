"""Loader"""

from typing import Any, Dict

from ..meta_data import ProtocolMetaData

from .fields import parse_fields
from .messages import parse_messages, parse_header, parse_components


def load_protocol(
        config: Dict[str, Any],
        *,
        is_millisecond_time: bool = True,
        is_float_decimal: bool = False,
        is_bool_enum: bool = False
) -> ProtocolMetaData:
    """Load a protocol

    Args:
        filename (str): The filename
        is_millisecond_time (bool, optional): If true times have milliseconds.
            Defaults to True.
        is_float_decimal (bool, optional): If true use Decimal for floating
            point numbers. Defaults to False.
        is_bool_enum (bool, optional): If true use enum names for booleans.
            Defaults to False.

    Returns:
        ProtocolMetaData: The protocol meta data.
    """
    version = config['version']['major'] + '.' + config['version']['minor']
    begin_string = config['beginString'].encode('ascii')
    fields = parse_fields(config['fields'])
    components = parse_components(config['components'], fields)
    messages = parse_messages(config['messages'], fields, components)
    header = parse_header(config['header'], fields, components)
    trailer = parse_header(config['trailer'], fields, components)

    return ProtocolMetaData(
        version,
        begin_string,
        fields,
        components,
        messages,
        header,
        trailer,
        is_millisecond_time=is_millisecond_time,
        is_float_decimal=is_float_decimal,
        is_bool_enum=is_bool_enum
    )
