from typing import Optional, Dict, Any, override
from data.base_classes.model import Model
from enum import Enum


class Shift(Enum):
    L = 1 # Libur
    P = 2 # Pagi
    M = 3 # Malam
    S = 4 # Siang


class Schedule(Model):
    def __init__(
        self,
        user_id: int,
        shift: Shift,
        day: int,
        id: Optional[int] = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.shift = shift
        self.day = day

    @override
    def get_id(self) -> Optional[int]:
        return self.id

    @override
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "id": self.id,
            "user_id": self.user_id,
            "shift": self.shift.name,
            "day": self.day,
        }
        return result
