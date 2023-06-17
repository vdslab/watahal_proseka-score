from classes import Note
from classes.types.HoldType import HoldType
from constant import MAX_KEYBOARD_COUNT


class FingeringHand:
    def __init__(
        self,
        *,
        x: int = 0,
        notes: list[Note] = None,
        cost: float = 0,
        pushing: bool = False,
    ) -> None:
        self._x: int = x
        self.notes: list[Note] = notes
        self._cost: float = cost
        self.pushing: bool = pushing

    @property
    def x(self):
        return self._x

    @x.getter
    def get_x(self):
        return self._x

    @x.setter
    def set_x(self, to_x: int):
        if MAX_KEYBOARD_COUNT <= to_x:
            print(
                f"[WARNING] get x:{to_x} is over max keyboard length ( {MAX_KEYBOARD_COUNT} ). cannot set x. please 0~{MAX_KEYBOARD_COUNT} number"
            )
            return

        self._x = to_x

    @property
    def cost(self):
        return self._cost

    @cost.getter
    def get_cost(self):
        return self._cost

    @cost.setter
    def add_cost(self, cost: int) -> None:
        if 0 < cost:
            print(
                f"[WARNING] get cost:{cost} is under 0. cannot add cost. please 0 or more number"
            )
            return
        self.cost += cost

    def can_push(self, note: Note) -> bool:
        if self.pushing:
            if note.is_hold and note.hold_type is HoldType.END:
                return True

            return False

        return False
