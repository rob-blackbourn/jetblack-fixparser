"""FIX message"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, MutableMapping, Optional, cast

from ..meta_data import (
    ProtocolMetaData,
    MessageMetaData
)

from .encoder import encode, SOH
from .decoder import decode, find_message_meta_data


class FixMessage:
    """A class which wraps a message in the form of a dictionary"""

    def __init__(
            self,
            protocol: ProtocolMetaData,
            message: Mapping[str, Any],
            meta_data: Optional[MessageMetaData] = None
    ) -> None:
        """Initialise the FIX message

        Args:
            protocol (ProtocolMetaData): The protocol meta data.
            message (Mapping[str, Any]): The fix message in the form of a
                mapping of message names to values.
            meta_data (Optional[MessageMetaData], optional): Optional meta data.
                If this is not supplied it will be discovered from the protocol
                meta data. Defaults to None.
        """
        self.protocol = protocol
        self.message = cast(MutableMapping[str, Any], deepcopy(message))
        self.meta_data = meta_data or find_message_meta_data(protocol, message)

    def encode(
            self,
            sep: bytes = SOH,
            regenerate_integrity: bool = True,
            convert_sep_for_checksum: bool = False
    ) -> bytes:
        """Encode the message into the FIX bytes buffer

        Args:
            sep (bytes, optional): The field separator. Defaults to SOH.
            regenerate_integrity (bool, optional): If true regenerate the
                integrity of the message by creating the begin string, body
                length, and checksum. Defaults to True.
            convert_sep_for_checksum (bool, optional): If true convert the field
                separator before calculating the checksum. Defaults to False.

        Returns:
            bytes: The FIX bytes buffer.
        """
        return encode(
            self.protocol,
            self.message,
            self.meta_data,
            sep=sep,
            regenerate_integrity=regenerate_integrity,
            convert_sep_for_checksum=convert_sep_for_checksum
        )

    @classmethod
    def decode(
            cls,
            protocol: ProtocolMetaData,
            buffer: bytes,
            *,
            strict: bool = True,
            validate: bool = True,
            sep: bytes = SOH,
            convert_sep_for_checksum: bool = True
    ) -> FixMessage:
        """Decode a FIX bytes buffer.

        Args:
            protocol (ProtocolMetaData): The protocol meta data.
            buffer (bytes): The FIX bytes buffer.
            strict (bool, optional): If true apply strict validation. Defaults
                to True.
            validate (bool, optional): If true validate the message. Defaults to
                True.
            sep (bytes, optional): The field separator. Defaults to SOH.
            convert_sep_for_checksum (bool, optional): If true convert the
                separator before calculating the checksum. Defaults to True.

        Returns:
            FixMessage: A class containing the decoded message.
        """
        message, meta_data = decode(
            protocol,
            buffer,
            strict=strict,
            validate=validate,
            sep=sep,
            convert_sep_for_checksum=convert_sep_for_checksum
        )
        return FixMessage(protocol, message, meta_data)
