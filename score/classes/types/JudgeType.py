from enum import auto

from classes.types.TypeABC import TypeABC


class JudgeType(TypeABC):
    OFF = 0
    FLICK_UP = auto()
    FLICK_DOWN = auto()
    FLICK_LEFT = auto()
    FLICK_RIGHT = auto()
    PUSH = auto()
    HOLD = auto()
