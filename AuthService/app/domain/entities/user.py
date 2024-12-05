from dataclasses import dataclass

from domain.events.user import UserRegisteredEvent
from domain.values.role import Role
from domain.values.email import Email
from domain.values.login import Login
from domain.values.password import Password
from domain.entities.base import BaseEntity


@dataclass
class User(BaseEntity):
    login: Login
    password: Password
    email: Email | None = None
    role: Role = Role('CUSTOMER')
    active: bool = True
    
    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'User') -> bool:
        return self.oid == __value.oid
    
    @classmethod
    def register_user(
        cls, 
        login: str,
        password: str,
        email: str | None = None,
        role: str = 'CUSTOMER',
        active: bool = True
    ) -> 'User':        
        
        user = User(
            login=Login(login),
            password=Password.hashed_password(password),
            role=Role(role),
            active=active
        )
        if email is not None:
            user.email = Email(email)
        
        
        user.register_event(
            UserRegisteredEvent(
                user_oid=user.oid,
                login=user.login,
                password=user.password,
                email=user.email,
                role=user.role,
                active=user.active
            )
        )
                
        return user
    
    
    