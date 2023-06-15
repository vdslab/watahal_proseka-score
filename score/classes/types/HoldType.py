from enum import auto

from classes.types.TypeABC import TypeABC


class NotesType(TypeABC):
    NONE = 0
    START = auto()
    END = auto()
    MIDDLE = auto()
