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
        self.fingering: list[dict[str, int]] = None

    def __str__(self):
        return f"FingeringHand; cost:{self.__cost}, notes:{self.__notes}"

    def to_dict(self):
        return {"cost": self.__cost, "notes": [note.to_dict() for note in self.__notes]}

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
        if cost < 0:
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

    def link_fingering(self, note: Note, separate: bool = False) -> None:
        self.__x = note.x
        self.pushing = note.type == NotesType.HOLD and (
            note.hold_type == HoldType.START or note.hold_type == HoldType.MIDDLE
        )
        if self.fingering is None:
            self.fingering = []
            self.fingering.append({"start": None, "end": note.id})
            return

        last_fingering = self.fingering[-1]
        if separate:
            self.fingering.append({"start": last_fingering["start"], "end": note.id})
        else:
            self.fingering.append({"start": last_fingering["end"], "end": note.id})

    def can_push(self, note: Note) -> bool:
        if not self.pushing:
            return True

        if not note.is_hold:
            return False

        if note.hold_type is HoldType.START or note.hold_type is HoldType.NONE:
            return False

        if self.__notes is not None and note.hole == self.__notes[-1].hole:
            return True
        else:
            return False
