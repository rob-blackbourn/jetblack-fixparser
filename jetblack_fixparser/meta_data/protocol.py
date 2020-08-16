"""The FIX protocol meta data"""

from typing import Mapping

from .message_member import FieldMetaData, ComponentMetaData, MessageMemberMetaData
from .message import MessageMetaData


class ProtocolMetaData:
    """FIX protocol meta data"""

    def __init__(
            self,
            version: str,
            begin_string: bytes,
            fields: Mapping[str, FieldMetaData],
            components: Mapping[str, ComponentMetaData],
            messages: Mapping[str, MessageMetaData],
            header: Mapping[str, MessageMemberMetaData],
            trailer: Mapping[str, MessageMemberMetaData],
            *,
            is_millisecond_time: bool = True,
            is_float_decimal: bool = False,
            is_bool_enum: bool = False
    ) -> None:
        """Initialise the FIX protocol meta data.

        Args:
            version (str): The version.
            begin_string (bytes): The begin string
            fields (Mapping[str, FieldMetaData]): Field definitions
            components (Mapping[str, ComponentMetaData]): Component definitions
            messages (Mapping[str, MessageMetaData]): Messages
            header (Mapping[str, MessageMemberMetaData]): The header meta data
            trailer (Mapping[str, MessageMemberMetaData]): The trailer meta data
            is_millisecond_time (bool, optional): If true the time has
                millisecond accuracy. Defaults to True.
            is_float_decimal (bool, optional): If true use Decimal to represent
                floating point values. Defaults to False.
            is_bool_enum (bool, optional): If true use enum names for boolean
                values. Defaults to False.
        """
        self.version = version
        self.begin_string = begin_string
        self.fields_by_name = fields
        self.fields_by_number = {
            field.number: field
            for field in fields.values()
        }
        self.components = components
        self.messages_by_name = messages
        self.messages_by_type = {
            message.msgtype: message
            for message in messages.values()
        }
        self.header = header
        self.trailer = trailer
        self.is_millisecond_time = is_millisecond_time
        self.is_float_decimal = is_float_decimal
        self.is_bool_enum = is_bool_enum

    def is_valid_message_name(self, name: str) -> bool:
        """Check if the name is a valid message name

        Args:
            name (str): The name to check.

        Raises:
            ValueError: If there are no message names found.

        Returns:
            bool: True if the name was a valid message name
        """
        message_type_field = self.fields_by_name['MsgType']
        if message_type_field.values_by_name is None:
            raise ValueError('No messages names in protocol')
        return name in message_type_field.values_by_name

    def __str__(self) -> str:
        return f'<ProtocolMetaData: version="{self.version}", begin_string={self.begin_string}'

    __repr__ = __str__
