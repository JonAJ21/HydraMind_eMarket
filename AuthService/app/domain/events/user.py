from dataclasses import dataclass

from domain.values.email import Email
from domain.values.password import Password
from domain.values.role import Role
from domain.values.login import Login
from domain.events.base import BaseEvent

@dataclass
class UserRegisteredEvent(BaseEvent):
    user_oid: str
    login: str
    password: bytes
    email: str | None = None
    role: str = 'CUSTOMER'
    active: bool = True