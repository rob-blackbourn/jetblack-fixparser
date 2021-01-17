"""A loader for QuickFix metadata (XML format)"""

from typing import Any, Dict, Mapping, Optional
import xml.dom.minidom as minidom
import xml.dom as dom

from ..meta_data import ProtocolMetaData
from ..types import ValueType

from .loader import load_protocol


def _process_members(node: Any) -> Dict[str, Any]:
    members: Dict[str, Any] = {}
    for child in node.childNodes:
        if child.nodeType != dom.Node.ELEMENT_NODE:
            continue

        if child.nodeName == 'field':
            members[child.attributes['name'].value] = {
                'type': 'field',
                'required': child.attributes['required'].value == 'Y'
            }
        elif child.nodeName == 'group':
            members[child.attributes['name'].value] = {
                'type': 'group',
                'required': child.attributes['required'].value == 'Y',
                'fields': _process_members(child)
            }
        elif child.nodeName == 'component':
            members[child.attributes['name'].value] = {
                'type': 'component',
                'required': child.attributes['required'].value == 'Y'
            }
        else:
            raise RuntimeError(f'invalid member node {child.nodeName}')
    return members


def _process_message(node: Any) -> Dict[str, Any]:
    return {
        'msgtype': node.attributes['msgtype'].value,
        'msgcat': node.attributes['msgcat'].value,
        'fields': _process_members(node)
    }


def _process_field(node: Any) -> Dict[str, Any]:
    return {
        'number': node.attributes['number'].value,
        'type': node.attributes['type'].value,
        'values': {
            child.attributes['enum'].value: child.attributes['description'].value
            for child in node.childNodes if child.nodeType == dom.Node.ELEMENT_NODE
        }
    }


def _process_messages(node: Any) -> Dict[str, Any]:
    return {
        child.attributes['name'].value: _process_message(child)
        for child in node.childNodes
        if child.nodeType == dom.Node.ELEMENT_NODE and child.nodeName == 'message'
    }


def _process_components(node: Any) -> Dict[str, Any]:
    return {
        child.attributes['name'].value: _process_members(child)
        for child in node.childNodes
        if child.nodeType == dom.Node.ELEMENT_NODE and child.nodeName == 'component'
    }


def _process_fields(node: Any) -> Dict[str, Any]:
    return {
        child.attributes['name'].value: _process_field(child)
        for child in node.childNodes
        if child.nodeType == dom.Node.ELEMENT_NODE and child.nodeName == 'field'
    }


def _process_root(node: Any) -> Dict[str, Any]:
    major = node.attributes['major'].value
    minor = node.attributes['minor'].value
    servicepack = node.attributes['servicepack'].value
    protocol = {
        'version': {
            'major': major,
            'minor': minor,
            'servicepack': servicepack
        },
        'beginString': 'FIX.' + major + '.' + minor,
        'fields': {},
        'components': {},
        'header': {},
        'trailer': {},
        'messages': {}
    }

    for child in node.childNodes:
        if child.nodeType != dom.Node.ELEMENT_NODE:
            continue

        if child.nodeName == 'header':
            protocol['header'] = _process_members(child)
        elif child.nodeName == 'trailer':
            protocol['trailer'] = _process_members(child)
        elif child.nodeName == 'messages':
            protocol['messages'] = _process_messages(child)
        elif child.nodeName == 'components':
            protocol['components'] = _process_components(child)
        elif child.nodeName == 'fields':
            protocol['fields'] = _process_fields(child)
        else:
            raise RuntimeError(f'unknown node {child.nodeName}')

    return protocol


def _convert_xml_file_to_dict(filename: str) -> Dict[str, Any]:
    document = minidom.parse(filename)
    config = _process_root(document.documentElement)
    return config


def load_quickfix_protocol(
        filename: str,
        *,
        is_millisecond_time: bool = True,
        is_float_decimal: bool = False,
        is_type_enum: Optional[Mapping[ValueType, bool]] = None
) -> ProtocolMetaData:
    """Load a QuickFix style XML protocol file

    Args:
        filename (str): The filename
        is_millisecond_time (bool, optional): If true times have milliseconds.
            Defaults to True.
        is_float_decimal (bool, optional): If true use Decimal for floating
            point numbers. Defaults to False.
        is_type_enum (Optional[Mapping[ValueType, bool]], optional): A map of
            types to control serialization to enums. Defaults to None.

    Returns:
        ProtocolMetaData: The protocol meta data.
    """

    config: Dict[str, Any] = _convert_xml_file_to_dict(filename)
    return load_protocol(
        config,
        is_millisecond_time=is_millisecond_time,
        is_float_decimal=is_float_decimal,
        is_type_enum=is_type_enum
    )
