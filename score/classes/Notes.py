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
        hole=0,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.type = type
        self.judge_type = judge_type
        self.is_yellow = is_yellow
        self.hold_type = hold_type
        self.hole = hole

    def __str__(self) -> str:
        describe = "Note describe:"
        pos = f"pos: (x, y) = ({self.x}, {self.y})"
        width = f"width: {self.width}"
        types = f"note type: {self.type.name} {'' if not self.is_hold else  f'{self.hold_type.name}: hole {self.hole}'}"
        judge = f"how judge: {self.judge_type.name}"

        return "\n\t".join([describe, pos, width, types, judge])

    @property
    def is_hold(self):
        return self.type == NotesType.HOLD
