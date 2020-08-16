"""Utils"""

from typing import ValuesView, Iterator, cast

from .message_member import MessageMemberMetaData, ComponentMetaData


def message_member_iter(
        message_members: ValuesView[MessageMemberMetaData]
) -> Iterator[MessageMemberMetaData]:
    """An iterator for message members

    Args:
        message_members (ValuesView[MessageMemberMetaData]): The members of the message

    Yields:
        Iterator[MessageMemberMetaData]: The next message member.
    """
    for message_member in message_members:
        if message_member.type == 'component':
            component = cast(ComponentMetaData, message_member.member)
            yield from message_member_iter(component.members.values())
        else:
            yield message_member
