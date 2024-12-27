from dataclasses import dataclass

from domain.entities.base import BaseEntity
from datetime import datetime

@dataclass
class Notification(BaseEntity):
    user_id: str
    text: str
    is_readed: bool
    time_created: datetime = datetime.now()
    
    
    