from functools import lru_cache
from fastapi.security import HTTPBearer
from punq import Container, Scope

from logic.commands.refresh import RefreshTokenCommand, RefreshTokenCommandHandler
from logic.services.user import BaseUserService, JWTUserService
from logic.services.auth import BaseAuthService, JWTAuthService
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
    container.register(BaseAuthService, JWTAuthService, scope=Scope.singleton)
    container.register(BaseUserService, JWTUserService, scope=Scope.singleton)
    
    container.register(RegisterUserCommandHandler)
    container.register(LoginUserCommandHandler)
    container.register(RefreshTokenCommandHandler)
    
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
        mediator.register_command(
            RefreshTokenCommand,
            [container.resolve(RefreshTokenCommandHandler)]
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
    
