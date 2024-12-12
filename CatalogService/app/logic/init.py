
from functools import lru_cache
from punq import Container, Scope

from infrastructure.repositories.notification import BaseCatalogRepository, PostgreCatalogRepository
from logic.mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()

def _init_container() -> Container:
    container = Container()
    
    # container.register(BaseNotificationService, RESTNotificationService, scope=Scope.singleton)
    
    # container.register(AddNotificationCommandHandler)
    
    
    
    def init_mediator():
        mediator = Mediator()
        
        # mediator.register_command(
        #     AddNotificationCommand,
        #     [container.resolve(AddNotificationCommandHandler)]
        # )
        
        
        
        return mediator
    
    container.register(Mediator, factory=init_mediator)
    
    def init_postgre_catalog_repository():
        repository = PostgreCatalogRepository()    
        return repository
        
    container.register(BaseCatalogRepository, factory=init_postgre_catalog_repository, scope=Scope.singleton)
    
    return container
    
