from dataclasses import dataclass

from domain.events.base import BaseEvent
from domain.entities.user import User


@dataclass
class NewUserAddedEvent(BaseEvent):
    user: User
    
    
    