
from functools import lru_cache
from punq import Container, Scope

from logic.commands.adress import AddAdressCommand, AddAdressCommandHandler
from logic.commands.email import ChangeEmailCommand, ChangeEmailCommandHandler
from logic.queries.get_user import GetUserInfoQuery, GetUserInfoQueryHandler
from logic.services.user import BaseUserService
from logic.services.user import RESTUserService
from infrastructure.repositories.users import BaseUsersRepository, PostgreUsersRepository
from logic.mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()

def _init_container() -> Container:
    container = Container()
    
    container.register(BaseUserService, RESTUserService, scope=Scope.singleton)
    
    container.register(GetUserInfoQueryHandler)
    container.register(ChangeEmailCommandHandler)
    container.register(AddAdressCommandHandler)
    
    
    def init_mediator():
        mediator = Mediator()
        
        mediator.register_query(
            GetUserInfoQuery,
            [container.resolve(GetUserInfoQueryHandler)]
        )
        
        mediator.register_command(
            ChangeEmailCommand,
            [container.resolve(ChangeEmailCommandHandler)]
        )
        
        mediator.register_command(
            AddAdressCommand,
            [container.resolve(AddAdressCommandHandler)]
        )
        
        return mediator
    
    container.register(Mediator, factory=init_mediator)
    
    def init_postgre_users_repository():
        repository = PostgreUsersRepository()
        
        return repository
        
    container.register(BaseUsersRepository, factory=init_postgre_users_repository, scope=Scope.singleton)
    
    return container
    