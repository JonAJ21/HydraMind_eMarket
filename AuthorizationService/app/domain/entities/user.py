from dataclasses import dataclass

from domain.values.role import Role
from domain.entities.base import BaseEntity
from domain.values.email import Email
from domain.values.login import Login
from domain.values.password import Password


@dataclass
class User(BaseEntity):
    login: Login
    password: Password
    email: Email
    role: Role
    
    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'User') -> bool:
        return self.oid == __value.oid