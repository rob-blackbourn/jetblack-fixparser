"""A loader for YAML formated metadata"""

from ruamel.yaml import YAML

from ..meta_data import ProtocolMetaData

from .loader import load_protocol


def load_yaml_protocol(
        filename: str,
        *,
        is_millisecond_time: bool = True,
        is_float_decimal: bool = False,
        is_bool_enum: bool = False
) -> ProtocolMetaData:
    """Load a YAML style protocol file

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
    yaml = YAML()
    with open(filename, 'rt') as file_ptr:
        return load_protocol(
            yaml.load(file_ptr),
            is_millisecond_time=is_millisecond_time,
            is_float_decimal=is_float_decimal,
            is_bool_enum=is_bool_enum
        )
