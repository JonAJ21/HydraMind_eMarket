from punq import Container, Scope

from infrastructure.repositories.user import BaseUsersRepository, MemoryUsersRepository
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(BaseUsersRepository, MemoryUsersRepository, scope=Scope.singleton)
    return container
    