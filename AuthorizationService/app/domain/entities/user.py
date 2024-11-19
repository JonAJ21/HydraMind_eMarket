from dataclasses import dataclass, field
from uuid import uuid4

#from domain.entities.base import BaseEntity
from domain.values.email import Email
from domain.values.password import Password
from domain.values.login import Login
from domain.values.role import Role

@dataclass
class User:
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True
    )
    login: Login
    password: Password
    email: Email
    role: Role
    
    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'User') -> bool:
        return self.oid == __value.oid
    
    
    