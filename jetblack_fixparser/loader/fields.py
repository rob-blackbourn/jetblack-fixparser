"""Fields"""

from typing import Mapping, Any, Union
from ..meta_data import FieldMetaData


def _to_number_as_bytes(number: Union[str, int]) -> bytes:
    if isinstance(number, int):
        number = str(number)
    return number.encode('ascii')


def _to_field_meta_data(name: str, info: Mapping[str, Any]) -> FieldMetaData:
    values = {
        str(value).encode('ascii'): str(description)
        for value, description in info['values'].items()
    } if 'values' in info and info['values'] else None

    return FieldMetaData(
        name,
        _to_number_as_bytes(info['number']),
        info['type'],
        values
    )


def parse_fields(fields: Mapping[str, Any]) -> Mapping[str, FieldMetaData]:
    """Parse fields

    Args:
        fields (Mapping[str, Any]): The fields to parse.

    Returns:
        Mapping[str, FieldMetaData]: The parsed fields.
    """
    return {
        name: _to_field_meta_data(name, info)
        for name, info in fields.items()
    }
