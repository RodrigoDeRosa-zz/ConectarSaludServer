from dataclasses import dataclass


@dataclass
class Affiliate:
    dni: str
    first_name: str
    last_name: str
    plan: str
    id: str
    sex: str
    age: int
    device_id: str

