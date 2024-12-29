"""Meta data for the FIX message"""

from typing import Mapping, Union

from .message_member import MessageMemberMetaData

MessageFieldMetaDataMapping = Mapping[
    str,
    Union[MessageMemberMetaData, 'MessageFieldMetaDataMapping']
]


class MessageMetaData:
    """FIX message meta data"""

    def __init__(
            self,
            name: str,
            msgtype: bytes,
            msgcat: str,
            fields: MessageFieldMetaDataMapping
    ) -> None:
        """Initialise the message meta data

        Args:
            name (str): The name
            msgtype (bytes): The type
            msgcat (str): The category
            fields (MessageFieldMetaDataMapping): The fields.
        """
        self.name = name
        self.msgtype = msgtype
        self.msgcat = msgcat
        self.fields = fields

    def __str__(self) -> str:
        return (
            'MessageMetaData: '
            'name="{name}", '
            'msgtype="{msgtype}", '
            'msgcat="{msgcat}"'
        ).format(
            name=self.name,
            msgtype=self.msgtype.decode('ascii'),
            msgcat=self.msgcat
        )

    __repr__ = __str__
