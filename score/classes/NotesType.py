from enum import Enum, auto


class NotesType(Enum):
    NORMAL = 1
    YELLOW = auto()
    HOLD = auto()
    FLICK = auto()

    def lower_name(self):
        return self.name.lower()
