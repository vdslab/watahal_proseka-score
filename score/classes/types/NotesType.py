from enum import Enum, auto

from .TypeABC import TypeABC


class NotesType(TypeABC):
    NONE = 0
    NORMAL = auto()
    YELLOW = auto()
    HOLD = auto()
    FLICK = auto()
