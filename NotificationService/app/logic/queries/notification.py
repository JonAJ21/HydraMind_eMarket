

from dataclasses import dataclass
from typing import List

from domain.entities.notification import Notification
from logic.services.notification import BaseNotificationService
from logic.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetLimitNotificationsQuery(BaseQuery):
    token: str
    count_limit: int
    
@dataclass(frozen=True)
class GetLimitNotificationsQueryHandler(QueryHandler[GetLimitNotificationsQuery, List[Notification]]):
    notification_service: BaseNotificationService
   
    async def handle(self, query: GetLimitNotificationsQuery) -> List[Notification]:
        return await self.notification_service.get_limit_notifications(query.token, query.count_limit)
    

@dataclass(frozen=True)
class GetUnreadNotificationsQuery(BaseQuery):
    token: str
    
@dataclass(frozen=True)
class GetUnreadNotificationsQueryHandler(QueryHandler[GetUnreadNotificationsQuery, List[Notification]]):
    notification_service: BaseNotificationService
   
    async def handle(self, query: GetUnreadNotificationsQuery) -> List[Notification]:
        return await self.notification_service.get_unread_notifications(query.token)