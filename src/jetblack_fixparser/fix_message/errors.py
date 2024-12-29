"""Errors for FIX message parsing"""

from ..meta_data import FieldMetaData


class DecodingError(Exception):
    """A decoding error"""


class EncodingError(Exception):
    """An encoding error"""


class FieldValueError(DecodingError):
    """A field value error"""

    def __init__(self, field: FieldMetaData, expected: bytes, received: bytes) -> None:
        super().__init__(
            f'field {field.number!r} ("{field.name}" expected "{expected!r}" received "{received!r}"'
        )
        self.field = field
        self.expected = expected
        self.received = received


class InvalidFieldError(DecodingError):
    """An invalid field error"""

    def __init__(self, field: bytes, value: bytes) -> None:
        super().__init__(
            f'received unknown field "{field!r}" with value "{value!r}"')


class InvalidMsgTypeError(DecodingError):
    """An invalid message type error"""

    def __init__(self, msgtype: bytes) -> None:
        super().__init__(f'received unknown msgtype "{msgtype!r}"')
