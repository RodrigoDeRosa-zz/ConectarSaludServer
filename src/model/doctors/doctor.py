from dataclasses import dataclass
from typing import List, KeysView


@dataclass
class TimeTable:
    day: str
    from_time: str
    to_time: str


@dataclass
class Doctor:
    dni: str
    first_name: str
    last_name: str
    phone: str
    email: str
    specialties: List[str]
    availability_times: List[TimeTable]
    id: str = None

    @classmethod
    def fields(cls) -> KeysView:
        return cls.__annotations__.keys()
