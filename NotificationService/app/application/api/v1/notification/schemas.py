
from datetime import datetime
from typing import List
from pydantic import BaseModel

from domain.entities.notification import Notification


class AddNotificationRequestSchema(BaseModel):
    user_id: str
    text: str

class AddNotificationResponseSchema(BaseModel):
    notification_id: str
    user_id: str
    notification_text: str
    is_readed: bool
    time_created: datetime
    
    @classmethod
    def from_entity(cls, notification: Notification) -> 'AddNotificationResponseSchema':
        return AddNotificationResponseSchema(
            notification_id=notification.oid,
            user_id=notification.user_id,
            notification_text=notification.text,
            is_readed=notification.is_readed,
            time_created=notification.time_created
        )

class GetLimitNotificationsRequestSchema(BaseModel):
    token: str
    count_limit: int

class GetUnreadNotificationsRequestSchema(BaseModel):
    token: str

class GetNotificationResponseSchema(BaseModel):
    notification_id: str
    user_id: str
    notification_text: str
    is_readed: bool
    time_created: datetime
     
class GetNotificationsResponseSchema(BaseModel):
    data: List[GetNotificationResponseSchema]