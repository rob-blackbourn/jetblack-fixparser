"""FIX message factory"""

from datetime import datetime
from typing import Any, Mapping, Optional

from ..meta_data import ProtocolMetaData

from .fix_message import FixMessage, SOH


class FixMessageFactory:
    """A factory for encoding and decoding FIX messages"""

    def __init__(
            self,
            protocol: ProtocolMetaData,
            sender_comp_id: str,
            target_comp_id: str,
            *,
            strict: bool = True,
            validate: bool = True,
            sep: bytes = SOH,
            convert_sep_for_checksum: bool = True,
            header_kwargs: Optional[Mapping[str, Any]] = None
    ) -> None:
        """Initialise the message factory

        Args:
            protocol (ProtocolMetaData): The protocol meta data.
            sender_comp_id (str): The sender comp id.
            target_comp_id (str): The target comp id.
            strict (bool, optional): If true use strict validation. Defaults to
                True.
            validate (bool, optional): If true validate the message. Defaults to
                True.
            sep (bytes, optional): The field separator to use. Defaults to SOH.
            convert_sep_for_checksum (bool, optional): If true convert the field
                separator before calculating the checksum. Defaults to True.
            header_kwargs (Optional[Mapping[str, Any]], optional): Extra header
                args. Defaults to None.
        """
        self.protocol = protocol
        self.sender_comp_id = sender_comp_id
        self.target_comp_id = target_comp_id
        self.strict = strict
        self.validate = validate
        self.sep = sep
        self.convert_sep_for_checksum = convert_sep_for_checksum
        self.header_kwargs = header_kwargs

    def create(
            self,
            msg_type: str,
            msg_seq_num: int,
            sending_time: datetime,
            body_kwargs: Optional[Mapping[str, Any]] = None,
            header_kwargs: Optional[Mapping[str, Any]] = None,
            trailer_kwargs: Optional[Mapping[str, Any]] = None
    ) -> FixMessage:
        """Create a FIX message

        Args:
            msg_type (str): The message type.
            msg_seq_num (int): The message sequence number.
            sending_time (datetime): The sending time.
            body_kwargs (Optional[Mapping[str, Any]], optional): The message
                body. Defaults to None.
            header_kwargs (Optional[Mapping[str, Any]], optional): Extra header
                args. Defaults to None.
            trailer_kwargs (Optional[Mapping[str, Any]], optional): Extra
                trailer args. Defaults to None.

        Returns:
            FixMessage: The FIX message.
        """
        assert self.protocol.is_valid_message_name(msg_type)

        header_args = {
            'BeginString': self.protocol.begin_string,
            'MsgType': msg_type,
            'MsgSeqNum': msg_seq_num,
            'SenderCompID': self.sender_comp_id,
            'TargetCompID': self.target_comp_id,
            'SendingTime': sending_time
        }
        if self.header_kwargs:
            header_args.update(self.header_kwargs)
        if header_kwargs:
            header_args.update(header_kwargs)

        data = {
            name: header_args[name]
            for name in self.protocol.header.keys()
            if name in header_args
        }

        if body_kwargs:
            data.update(body_kwargs)

        if trailer_kwargs:
            data.update({
                name: header_args[name]
                for name in self.protocol.trailer.keys()
                if name in trailer_kwargs
            })

        return FixMessage(self.protocol, data)

    def decode(self, buffer: bytes) -> FixMessage:
        """Decode a FIX message byte buffer.

        Args:
            buffer (bytes): The FIX bytes buffer

        Returns:
            FixMessage: A decoded message.
        """
        return FixMessage.decode(
            self.protocol,
            buffer,
            strict=self.strict,
            validate=self.validate,
            sep=self.sep,
            convert_sep_for_checksum=self.convert_sep_for_checksum
        )
