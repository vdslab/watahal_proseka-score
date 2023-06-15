from classes.types.HoldType import HoldType
from classes.types.NotesType import NotesType


class Note:
    def __init__(
        self,
        *,
        x: int,
        y: int,
        width: int,
        type: NotesType,
        judge_type,
        is_yellow=False,
        hold_type: HoldType = None,
        hole=0
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.type = type
        self.judge_type = judge_type
        self.is_yellow = is_yellow
        self.hold_type = hold_type
        self.hole = hole

    @property
    def is_hold(self):
        return self.type == NotesType.HOLD
