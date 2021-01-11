""""Meta data for FIX message members"""

from __future__ import annotations

from typing import Mapping, Optional, Union


class FieldMetaData:
    """Field meta data"""

    def __init__(
            self,
            name: str,
            number: bytes,
            type_: str,
            values: Optional[Mapping[bytes, str]] = None
    ) -> None:
        """Initialise the field meta data

        Args:
            name (str): The name.
            number (bytes): The description
            type_ (str): The type
            values (Optional[Mapping[bytes, str]], optional): Enum values.
                Defaults to None.
        """
        self.name = name
        self.number = number
        self.type = type_
        self.values = values
        self.values_by_name = {
            value: name for name,
            value in values.items()
        } if values else None

    def __str__(self) -> str:
        return (
            'FieldMetaData: '
            'name="{name}", '
            'number="{number}", '
            'type="{type}", '
            'values={values}'
        ).format(
            name=self.name,
            number=self.number.decode('ascii'),
            type=self.type,
            values=None if self.values is None else {
                name.decode('ascii'): value
                for name, value in self.values.items()
            }
        )

    __repr__ = __str__


class ComponentMetaData:
    """Component meta data"""

    def __init__(
            self,
            name: str,
            members: Mapping[str, MessageMemberMetaData]
    ) -> None:
        """Initialise the component meta data.

        Args:
            name (str): The name
            members (Mapping[str, MessageMemberMetaData]): The members
        """
        self.name = name
        self.members = members

    def __str__(self) -> str:
        return 'ComponentMetaData: name="{name}", members={members}'.format(
            name=self.name,
            members=self.members
        )

    __repr__ = __str__


class MessageMemberMetaData:
    """The meta data for a message member"""

    def __init__(
            self,
            member: Union[FieldMetaData, ComponentMetaData],
            type_: str,
            is_required: bool,
            children: Optional[Mapping[str, MessageMemberMetaData]] = None
    ) -> None:
        """Initialise the member meta data

        Args:
            member (Union[FieldMetaData, ComponentMetaData]): The member
            type_ (str): The type (field, group, or component).
            is_required (bool): If true the member is required.
            children (Optional[Mapping[str, MessageMemberMetaData]], optional):
                Child members. Defaults to None.
        """
        self.member = member
        self.type = type_
        self.is_required = is_required
        self.children = children

    def __str__(self) -> str:
        return (
            'MessageMemberMetaData: '
            'member={member}, '
            'is_required={is_required}, '
            'children={children}'
        ).format(
            member=self.member,
            is_required=self.is_required,
            children=self.children
        )

    __repr__ = __str__


MessageFieldMetaDataMapping = Mapping[
    str,
    Union[MessageMemberMetaData, 'MessageFieldMetaDataMapping']
]
