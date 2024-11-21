from dataclasses import dataclass

from domain.values.email import Email
from domain.values.password import Password
from domain.values.role import Role
from domain.values.login import Login
from domain.events.base import BaseEvent

@dataclass
class NewUserAddedEvent(BaseEvent):
    user_oid: str
    login: str
    password: str
    email: str
    role: str
    
    
    