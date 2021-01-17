"""Types"""

from enum import Enum, auto


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
