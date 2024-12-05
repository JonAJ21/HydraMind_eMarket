from asyncio import get_running_loop, new_event_loop, run, set_event_loop
from functools import lru_cache
from asyncpg import create_pool
from punq import Container, Scope

# from settings.config import settings
from logic.commands.refresh import RefreshTokenCommand, RefreshTokenCommandHandler
from logic.services.user import BaseUserService, JWTUserService
from logic.services.auth import BaseAuthService, JWTAuthService
from logic.queries.user import GetUserInfoQuery, GetUserInfoQueryHandler
from logic.commands.login import LoginUserCommand, LoginUserCommandHandler
from logic.commands.register import RegisterUserCommand, RegisterUserCommandHandler
from logic.mediator import Mediator
from infrastructure.repositories.users import BaseUsersRepository, MemoryUsersRepository, PostgreUsersRepository


@lru_cache(1)
def init_container():
    return _init_container()

def _init_container() -> Container:
    container = Container()
    
    #container.register(BaseUsersRepository, MemoryUsersRepository, scope=Scope.singleton)
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
    
    # async def init_postgre_users_repository():
    #     repository = PostgreUsersRepository()
        
    #     await repository.init()
    #     return repository
    def init_postgre_users_repository():
        repository = PostgreUsersRepository()
        
        return repository
        
        
    
    
    
    container.register(BaseUsersRepository, factory=init_postgre_users_repository, scope=Scope.singleton)
    
    return container
    
