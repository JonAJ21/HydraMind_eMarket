from functools import lru_cache
from fastapi.security import HTTPBearer
from punq import Container, Scope

from logic.queries.user import GetUserInfoQuery, GetUserInfoQueryHandler
from logic.commands.login import LoginUserCommand, LoginUserCommandHandler
from logic.commands.register import RegisterUserCommand, RegisterUserCommandHandler
from logic.mediator import Mediator
from infrastructure.repositories.users import BaseUsersRepository, MemoryUsersRepository


@lru_cache(1)
def init_container():
    return _init_container()

def _init_container() -> Container:
    container = Container()
    
    container.register(BaseUsersRepository, MemoryUsersRepository, scope=Scope.singleton)
    
    container.register(RegisterUserCommandHandler)
    container.register(LoginUserCommandHandler)
    container.register(GetUserInfoQueryHandler)
    
    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            RegisterUserCommand,
            [container.resolve(RegisterUserCommandHandler)]
        )
        mediator.register_command(
            LoginUserCommand,
            [container.resolve(LoginUserCommandHandler)]
        )
        mediator.register_query(
            GetUserInfoQuery,
            [container.resolve(GetUserInfoQueryHandler)]
        )
        return mediator
    
    container.register(Mediator, factory=init_mediator)
    
    # def init_bearer():
    #     return HTTPBearer()
    
    # container.register(Mediator, factory=init_bearer)
    
    
    return container
    
