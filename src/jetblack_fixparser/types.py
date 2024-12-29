"""Types"""

from enum import Enum, Flag, auto


class ValueType(Enum):
    """Value types"""
    INT = auto()
    SEQNUM = auto()
    NUMINGROUP = auto()
    LENGTH = auto()
    FLOAT = auto()
    QTY = auto()
    PRICE = auto()
    PRICEOFFSET = auto()
    AMT = auto()
    CHAR = auto()
    STRING = auto()
    CURRENCY = auto()
    EXCHANGE = auto()
    BOOLEAN = auto()
    MULTIPLEVALUESTRING = auto()
    UTCTIMESTAMP = auto()
    UTCTIMEONLY = auto()
    LOCALMKTDATE = auto()
    UTCDATE = auto()
    MONTHYEAR = auto()
    DAYOFMONTH = auto()


class StrictMode(Flag):
    """Specific categories of strictness"""
    NONE = 0
    ENSURE_REQUIRED = auto()
    ENSURE_GROUP_ORDER = auto()
    ALL = ENSURE_REQUIRED | ENSURE_GROUP_ORDER
