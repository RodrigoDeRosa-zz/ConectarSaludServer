from dataclasses import dataclass
from typing import List, KeysView


@dataclass
class TimeTable:
    day: str
    from_time: str
    to_time: str


@dataclass
class Doctor:
    id: str = None
    dni: str = None
    licence: str = None
    first_name: str = None
    last_name: str = None
    email: str = None
    centers: List[str] = None
    specialties: List[str] = None
    availability_times: List[TimeTable] = None

    @classmethod
    def fields(cls) -> KeysView:
        return cls.__annotations__.keys()
