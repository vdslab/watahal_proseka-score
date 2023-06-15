from classes.Notes import Note
from classes.types.HoldType import HoldType
from constant import MAX_KEYBOARD_COUNT


class FingeringHand:
    def __init__(self) -> None:
        self._x = 0
        self.notes = []
        self.cost = 0
        self.pushing = False

    def update_move_cost(self, to_x: int) -> None:
        if MAX_KEYBOARD_COUNT <= to_x:
            print(
                f"[WARNING] get x:{to_x} is over max keyboard length ( {MAX_KEYBOARD_COUNT} ). cannot update cost"
            )
            return

        self.cost = abs(self._x - to_x)

    def can_push(self, note: Note) -> bool:
        if self.pushing:
            if note.is_hold() and note.hold_type is HoldType.END:
                return True

            return False

        return False
