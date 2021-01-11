"""Messages"""

from typing import Any, Mapping, MutableMapping, Optional

from ..meta_data import FieldMetaData, ComponentMetaData, MessageMemberMetaData, MessageMetaData


def _to_message_member_meta_data(
        info: Mapping[str, Any],
        field_meta_data: Mapping[str, FieldMetaData],
        component_meta_data: Mapping[str, ComponentMetaData]
) -> Mapping[str, MessageMemberMetaData]:
    member: MutableMapping[str, MessageMemberMetaData] = {}

    for name, value in info.items():
        member_type = value.get('type', 'field') if value else 'field'
        is_required = value.get('required', False) if value else False

        if member_type == 'field':
            field = field_meta_data[name]
            member[name] = MessageMemberMetaData(
                field,
                member_type,
                is_required
            )
        elif member_type == 'group':
            field = field_meta_data[name]
            member[name] = MessageMemberMetaData(
                field,
                member_type,
                is_required,
                _to_message_member_meta_data(
                    value['fields'],
                    field_meta_data,
                    component_meta_data
                )
            )
        elif member_type == 'component':
            component = component_meta_data[name]
            member[name] = MessageMemberMetaData(
                component,
                member_type,
                is_required
            )
        else:
            raise RuntimeError(f'unknown type "{member_type}"')

    return member


def _to_message_meta_data(
        name: str,
        info: Mapping[str, Any],
        field_meta_data: Mapping[str, FieldMetaData],
        component_meta_data: Mapping[str, ComponentMetaData]
) -> MessageMetaData:
    return MessageMetaData(
        name,
        info['msgtype'].encode('ascii'),
        info['msgcat'],
        _to_message_member_meta_data(
            info['fields'] or {}, field_meta_data, component_meta_data)
    )


def parse_messages(
        messages: Mapping[str, Any],
        field_meta_data: Mapping[str, FieldMetaData],
        component_meta_data: Mapping[str, ComponentMetaData]
) -> Mapping[str, MessageMetaData]:
    """Parse messages.

    Args:
        messages (Mapping[str, Any]): The messages to parse.
        field_meta_data (Mapping[str, FieldMetaData]): The field metadata.
        component_meta_data (Mapping[str, ComponentMetaData]): The component
            metadata.

    Returns:
        Mapping[str, MessageMetaData]: The parsed message.
    """
    return {
        name: _to_message_meta_data(
            name, info, field_meta_data, component_meta_data)
        for name, info in messages.items()
    }


def parse_header(
        info: Mapping[str, Any],
        field_meta_data: Mapping[str, FieldMetaData],
        component_meta_data: Mapping[str, ComponentMetaData]
) -> Mapping[str, MessageMemberMetaData]:
    """Parse the header.

    Args:
        info (Mapping[str, Any]): The header.
        field_meta_data (Mapping[str, FieldMetaData]): The field metadata.
        component_meta_data (Mapping[str, ComponentMetaData]): The component
            metadata.

    Returns:
        Mapping[str, MessageMemberMetaData]: The parsed header.
    """
    return _to_message_member_meta_data(info, field_meta_data, component_meta_data)


def parse_components(
        info: Optional[Mapping[str, Any]],
        field_meta_data: Mapping[str, FieldMetaData]
) -> Mapping[str, ComponentMetaData]:
    """Parse the components.

    Args:
        info (Optional[Mapping[str, Any]]): The components
        field_meta_data (Mapping[str, FieldMetaData]): The field metadata.

    Returns:
        Mapping[str, ComponentMetaData]: The parsed components.
    """
    if info is None:
        return dict()

    # Declare components first to handle forward references.
    components = {
        name: ComponentMetaData(name, {})
        for name in info.keys()
    }
    for name, data in info.items():
        component = components[name]
        component.members = _to_message_member_meta_data(
            data,
            field_meta_data,
            components
        )
    return components
