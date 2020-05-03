from dataclasses import dataclass
from typing import List, KeysView

from src.model.doctors.time_table import TimeTable


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
