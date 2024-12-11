
from functools import lru_cache
from punq import Container, Scope

from logic.mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()

def _init_container() -> Container:
    container = Container()
    
    def init_mediator():
        mediator = Mediator()
        
        return mediator
    
    container.register(Mediator, factory=init_mediator)
    
    # def init_postgre_users_repository():
    #     repository = PostgreUsersRepository()
        
    #     return repository
        
    # container.register(BaseUsersRepository, factory=init_postgre_users_repository, scope=Scope.singleton)
    
    return container
    
