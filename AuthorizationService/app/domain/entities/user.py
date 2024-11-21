from dataclasses import dataclass

from domain.events.user import NewUserAddedEvent
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
    
    @classmethod
    def add_user(cls, login: Login, password: Password, email: Email, role: Role) -> 'User':        
        new_user = cls(login=login, password=password, email=email, role=role)
        new_user.register_event(
            NewUserAddedEvent(
                user_oid=new_user.oid,
                login=new_user.login,
                password=new_user.password,
                email=new_user.email,
                role=new_user.role
            )
        )
        return new_user