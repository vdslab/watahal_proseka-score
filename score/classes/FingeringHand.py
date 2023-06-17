from constant import MAX_KEYBOARD_COUNT

from .Notes import Note
from .types.HoldType import HoldType


class FingeringHand:
    def __init__(
        self,
        *,
        x: int = 0,
    ) -> None:
        self.__x: int = x
        self.__notes: list[tuple(int, Note)] = None
        self.__cost: float = 0
        self.pushing: bool = False

    @property
    def x(self):
        return self.__x

    @x.getter
    def get_x(self):
        return self.__x

    @x.setter
    def set_x(self, to_x: int):
        if MAX_KEYBOARD_COUNT <= to_x:
            print(
                f"[WARNING] get x:{to_x} is over max keyboard length ( {MAX_KEYBOARD_COUNT} ). cannot set x. please 0~{MAX_KEYBOARD_COUNT} number"
            )
            return

        self.__x = to_x

    @property
    def cost(self):
        return self.__cost

    @cost.getter
    def get_cost(self):
        return self.__cost

    @cost.setter
    def add_cost(self, cost: int) -> None:
        if 0 < cost:
            print(
                f"[WARNING] get cost:{cost} is under 0. cannot add cost. please 0 or more number"
            )
            return
        self.__cost += cost

    @property
    def notes(self) -> list[tuple[int, Note]]:
        return self.__notes

    @notes.setter
    def set_notes(self, value: tuple[int, Note]):
        try:
            index, note = value
            if type(value) == tuple or type(index) == int or type(note) == Note:
                raise TypeError

        except ValueError:
            raise ValueError("please set iterable two items (index, note)")
        except TypeError:
            raise TypeError("please set tuple of (int, Note) item")
        else:
            self.__notes.append(value)

    @notes.getter
    def get_notes(self) -> list[tuple[int, Note]]:
        return self.__notes

    def can_push(self, note: Note) -> bool:
        if self.pushing:
            if note.is_hold and note.hold_type is HoldType.END:
                return True

            return False

        return True
