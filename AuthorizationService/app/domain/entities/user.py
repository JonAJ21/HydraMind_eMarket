from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.values.email import Email
from domain.values.password import Password
from domain.values.login import Login
from domain.values.role import Role

@dataclass
class User(BaseEntity):
    login: Login
    password: Password
    email: Email
    role: Role
    
    
    
    
    