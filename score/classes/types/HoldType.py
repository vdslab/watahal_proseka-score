from enum import auto

from .TypeABC import TypeABC


class HoldType(TypeABC):
    NONE = 0
    START = auto()
    END = auto()
    MIDDLE = auto()
