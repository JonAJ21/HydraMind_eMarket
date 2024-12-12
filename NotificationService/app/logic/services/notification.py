from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import httpx

from logic.exceptions.user import BadRequestToAuthServiceException
from infrastructure.repositories.notification import BaseNotificationRepository
from domain.entities.notification import Notification
from settings.config import settings


@dataclass
class BaseNotificationService(ABC):
    
    @abstractmethod
    async def add_notification(self, user_id: str, text: str) -> Notification:
        ...
        
    @abstractmethod
    async def get_limit_notifications(self, token: str, count_limit: int) -> List[Notification]:
        ...
    
    @abstractmethod
    async def get_unread_notifications(self, token: str) -> List[Notification]:
        ...
    
    
@dataclass
class RESTNotificationService(BaseNotificationService):
    notification_repository: BaseNotificationRepository
    
    async def add_notification(self, user_id: str, text: str) -> Notification:
        notification = Notification(
            user_id=user_id,
            text=text,
            is_readed=False
        )
        await self.notification_repository.add_notification(notification=notification)
        
        return notification
    
    async def get_limit_notifications(self, token: str, count_limit: int) -> List[Notification]:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        user_id = response.json()['oid']
        
        return await self.notification_repository.get_limit_notifications(user_id, count_limit)
    
    async def get_unread_notifications(self, token: str) -> List[Notification]:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        user_id = response.json()['oid']
        
        return await self.notification_repository.get_unread_notifications(user_id)