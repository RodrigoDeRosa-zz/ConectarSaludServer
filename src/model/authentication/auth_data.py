from dataclasses import dataclass


@dataclass
class AuthData:
    user_id: str
    password: str
    role: str = None
