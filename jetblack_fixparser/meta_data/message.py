"""Meta data for the FIX message"""

from .message_member import MessageFieldMetaDataMapping


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
            f'name="{self.name}", '
            f'msgtype="{self.msgtype.decode("ascii")}", '
            f'msgcat="{self.msgcat}"'
        )

    __repr__ = __str__
