from dataclasses import dataclass


@dataclass
class AuthData:
    user_id: str
    password: str
    device_id: str
    role: str = None
