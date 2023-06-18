from constant import MAX_KEYBOARD_COUNT

from .Notes import Note
from .types import HoldType, NotesType


class FingeringHand:
    def __init__(
        self,
        *,
        x: int = 0,
    ) -> None:
        self.__x: int = x
        self.__notes: list[Note] = None
        self.__notes_index: list[int] = None
        self.__cost: float = 0
        self.pushing: bool = False

    @property
    def x(self):
        return self.__x

    @x.getter
    def get_x(self):
        return self.__x

    @property
    def cost(self):
        return self.__cost

    @cost.getter
    def get_cost(self):
        return self.__cost

    # @cost.setter
    def add_cost(self, cost: int) -> None:
        if 0 < cost:
            print(
                f"[WARNING] get cost:{cost} is under 0. cannot add cost. please 0 or more number"
            )
            return
        self.__cost += cost

    @property
    def notes(self) -> tuple[list[int], list[Note]]:
        return self.__notes_index, self.__notes

    @notes.getter
    def get_notes(self) -> tuple[list[int], list[Note]]:
        return self.__notes_index, self.__notes

    # @notes.setter
    def add_notes(self, value: tuple[int, Note]):
        try:
            index, note = value
            if type(index) != int or type(note) != Note:
                raise TypeError
        except ValueError:
            raise ValueError("please set iterable two items (int, Note)")
        except TypeError:
            raise TypeError("please set iterable of (int, Note) item")
        else:
            if self.__notes is None:
                self.__notes = []
            self.__notes.append(note)

            if self.__notes_index is None:
                self.__notes_index = []
            self.__notes_index.append(index)
            self.__x = note.x
            self.pushing = note.type == NotesType.HOLD and (
                note.hold_type == HoldType.START or note.hold_type == HoldType.MIDDLE
            )

    def can_push(self, note: Note) -> bool:
        if self.pushing:
            if note.is_hold and note.hold_type is HoldType.END:
                return True

            return False

        return True
