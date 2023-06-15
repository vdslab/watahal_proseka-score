from classes.types import HoldType, JudgeType, NotesType


class Note:
    def __init__(
        self,
        *,
        x: int,
        y: int,
        width: int,
        type: NotesType,
        judge_type: JudgeType,
        is_yellow=False,
        hold_type: HoldType = HoldType.NONE,
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

    def __eq__(self, __value: object) -> bool:
        return (
            __value is not None
            and type(self) == type(__value)
            and self.__dict__ == __value.__dict__
        )

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "type": self.type.lower_name(),
            "judge_type": self.judge_type.lower_name(),
            "is_yellow": self.type == NotesType.YELLOW,
            "hold_type": self.hold_type.lower_name(),
            "hole": self.hole,
        }

    @property
    def is_hold(self):
        return self.type == NotesType.HOLD
