from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from settings.config import settings
from domain.entities.notification import Notification

from asyncpg import Pool

@dataclass
class BaseNotificationRepository(ABC):
    
    @abstractmethod
    async def add_notification(self, notification: Notification) -> None:
        ...
        
    @abstractmethod
    async def get_limit_notifications(self, user_id: str, count_limit: int) -> List[Notification]:
        ...
        
    @abstractmethod
    async def get_unread_notifications(self, user_id: str) -> List[Notification]:
        ...
        
@dataclass
class PostgreNotificationRepository(BaseNotificationRepository):
    _connection_pool: Pool = settings.postgre_sql_pool.pool
    
    async def add_notification(self, notification: Notification) -> None:
        
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    INSERT INTO order_notifications
                        (notification_id, user_id, notification_text, is_readed, time_created)
                    VALUES ($1, $2, $3, $4, $5)
                '''
                
                await connection.execute(
                    query, notification.oid, notification.user_id,
                    notification.text, notification.is_readed, notification.time_created)
                
        return
                
                
    async def get_limit_notifications(self, user_id, count_limit) -> List[Notification]:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    UPDATE order_notifications
                    SET is_readed = TRUE
                    WHERE notification_id IN (SELECT notification_id
                                              FROM order_notifications
                                              WHERE user_id = $1
                                              ORDER BY time_created DESC
                                              LIMIT $2);
                '''
                
                await connection.execute(
                    query,
                    user_id,
                    count_limit
                )
                
                query = '''
                    SELECT notification_id, user_id, notification_text, is_readed, time_created
                    FROM order_notifications
                    WHERE user_id = $1
                    ORDER BY time_created DESC
                    LIMIT $2; 
                '''
                
                rows = await connection.fetch(
                    query,
                    user_id,
                    count_limit
                )
                
                notifications = []
                for row in rows:
                    notification = Notification(
                        oid=str(row['notification_id']),
                        user_id=str(user_id),
                        text=str(row['notification_text']),
                        is_readed=bool(row['is_readed']),
                        time_created=row['time_created']
                    )
                    notifications.append(notification)
                return notifications
    
    async def get_unread_notifications(self, user_id) -> List[Notification]:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT notification_id, user_id, notification_text, is_readed, time_created
                    FROM order_notifications
                    WHERE user_id = $1 AND is_readed = FALSE
                    ORDER BY time_created DESC; 
                '''
                
                rows = await connection.fetch(
                    query,
                    user_id
                )
                
                
                query = '''
                    UPDATE order_notifications
                    SET is_readed = TRUE
                    WHERE notification_id IN (SELECT notification_id
                                              FROM order_notifications
                                              WHERE user_id = $1 AND is_readed = FALSE
                                              ORDER BY time_created DESC
                                              );
                '''
                
                await connection.execute(
                    query,
                    user_id
                )
                
                
                notifications = []
                for row in rows:
                    notification = Notification(
                        oid=str(row['notification_id']),
                        user_id=str(user_id),
                        text=str(row['notification_text']),
                        is_readed=True,#bool(row['is_readed']),
                        time_created=row['time_created']
                    )
                    notifications.append(notification)
                    
                return notifications
                
                
                    
                
                
        
        
        
        