
from functools import lru_cache
from punq import Container, Scope

from logic.queries.notification import GetLimitNotificationsQuery, GetLimitNotificationsQueryHandler, GetUnreadNotificationsQuery, GetUnreadNotificationsQueryHandler
from logic.commands.notification import AddNotificationCommand, AddNotificationCommandHandler
from logic.services.notification import BaseNotificationService, RESTNotificationService
from infrastructure.repositories.notification import BaseNotificationRepository, PostgreNotificationRepository
from logic.mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()

def _init_container() -> Container:
    container = Container()
    
    container.register(BaseNotificationService, RESTNotificationService, scope=Scope.singleton)
    
    container.register(AddNotificationCommandHandler)
    container.register(GetLimitNotificationsQueryHandler)
    container.register(GetUnreadNotificationsQueryHandler)
    
    
    def init_mediator():
        mediator = Mediator()
        
        mediator.register_command(
            AddNotificationCommand,
            [container.resolve(AddNotificationCommandHandler)]
        )
        
        mediator.register_query(
            GetLimitNotificationsQuery,
            [container.resolve(GetLimitNotificationsQueryHandler)]
        )
        mediator.register_query(
            GetUnreadNotificationsQuery,
            [container.resolve(GetUnreadNotificationsQueryHandler)]
        )
        
        return mediator
    
    container.register(Mediator, factory=init_mediator)
    
    def init_postgre_notification_repository():
        repository = PostgreNotificationRepository()    
        return repository
        
    container.register(BaseNotificationRepository, factory=init_postgre_notification_repository, scope=Scope.singleton)
    
    return container
    
