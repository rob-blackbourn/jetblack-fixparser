"""A loader for YAML formatted metadata"""

from pathlib import Path
from typing import Mapping, Optional, Union

from ruamel.yaml import YAML

from ..meta_data import ProtocolMetaData
from ..types import ValueType

from .loader import load_protocol


def load_yaml_protocol(
        filename: Union[str, Path],
        *,
        is_millisecond_time: bool = True,
        is_float_decimal: bool = False,
        is_type_enum: Optional[Mapping[Union[ValueType, str], bool]] = None
) -> ProtocolMetaData:
    """Load a YAML style protocol file

    Args:
        filename (Union[str, Path]): The filename
        is_millisecond_time (bool, optional): If true times have milliseconds.
            Defaults to True.
        is_float_decimal (bool, optional): If true use Decimal for floating
            point numbers. Defaults to False.
        is_type_enum (Optional[Mapping[Union[ValueType, str], bool]], optional):
            Map controlling serialization to enums. Defaults to None.

    Returns:
        ProtocolMetaData: The protocol meta data.
    """
    if not isinstance(filename, Path):
        filename = Path(filename)

    yaml = YAML()

    with filename.open('rt', encoding="utf8") as file_ptr:
        return load_protocol(
            yaml.load(file_ptr),
            is_millisecond_time=is_millisecond_time,
            is_float_decimal=is_float_decimal,
            is_type_enum=is_type_enum
        )
