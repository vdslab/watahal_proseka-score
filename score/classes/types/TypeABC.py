from enum import Enum


class TypeABC(Enum):
    def lower_name(self) -> str:
        return self.name.lower()
