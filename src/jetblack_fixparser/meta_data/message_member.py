""""Meta data for FIX message members"""

from __future__ import annotations

from typing import Mapping


class FieldMetaData:
    """Field meta data"""

    def __init__(
            self,
            name: str,
            number: bytes,
            type_: str,
            values: Mapping[bytes, str] | None = None
    ) -> None:
        """Initialise the field meta data

        Args:
            name (str): The name.
            number (bytes): The description
            type_ (str): The type
            values (Mapping[bytes, str] | None, optional): Enum values.
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
        return (
            'ComponentMetaData: '
            f'name="{self.name}", '
            f'members={self.members}'
        )

    __repr__ = __str__


class MessageMemberMetaData:
    """The meta data for a message member"""

    def __init__(
            self,
            member: FieldMetaData | ComponentMetaData,
            type_: str,
            is_required: bool,
            children: Mapping[str, MessageMemberMetaData] | None = None
    ) -> None:
        """Initialise the member meta data

        Args:
            member (FieldMetaData | ComponentMetaData): The member
            type_ (str): The type (field, group, or component).
            is_required (bool): If true the member is required.
            children (Mapping[str, MessageMemberMetaData] | None, optional):
                Child members. Defaults to None.
        """
        self.member = member
        self.type = type_
        self.is_required = is_required
        self.children = children

    def __str__(self) -> str:
        return (
            'MessageMemberMetaData: '
            f'member={self.member}, '
            f'is_required={self.is_required}, '
            f'children={self.children}'
        )

    __repr__ = __str__


type MessageFieldMetaDataMapping = Mapping[
    str,
    MessageMemberMetaData | 'MessageFieldMetaDataMapping'
]
