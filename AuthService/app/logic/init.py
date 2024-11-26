from functools import lru_cache
from punq import Container, Scope

from logic.commands.auth import RegisterUserCommand, RegisterUserCommandHandler
from logic.mediator import Mediator
from infrastructure.repositories.users import BaseUsersRepository, MemoryUsersRepository


@lru_cache(1)
def init_container():
    return _init_container()

def _init_container() -> Container:
    container = Container()
    
    container.register(BaseUsersRepository, MemoryUsersRepository, scope=Scope.singleton)
    
    container.register(RegisterUserCommandHandler)
    
    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            RegisterUserCommand,
            [container.resolve(RegisterUserCommandHandler)]
        )
        return mediator
    
    container.register(Mediator, factory=init_mediator)
    
    return container
    
