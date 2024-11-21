from functools import lru_cache
from punq import Container, Scope

from infrastructure.repositories.user import BaseUsersRepository, MemoryUsersRepository
from logic.commands.user import AddUserCommand, AddUserCommandHandler
from logic.mediator import Mediator

    
@lru_cache(1)
def init_container():
    return _init_container()

def _init_container() -> Container:
    container = Container()
    
    container.register(BaseUsersRepository, MemoryUsersRepository, scope=Scope.singleton)
    container.register(AddUserCommandHandler)
    
    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            AddUserCommand,
            [container.resolve(AddUserCommandHandler)]
        )
        return mediator
    
    container.register(Mediator, factory=init_mediator)  
    
    return container
    