from dataclasses import dataclass, field
from uuid import uuid4

from domain.events.users import NewUserAddedEvent
from domain.entities.base import BaseEntity
from domain.entities.user import User
    
@dataclass
class Users(BaseEntity):
    users: set[User] = field(
        default_factory=set,
        kw_only=True
    )
    
    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'Users') -> bool:
        return self.oid == __value.oid
    
    def add_user(self, user: User):
        self.users.add(user)
        self.register_event(NewUserAddedEvent(user=user))