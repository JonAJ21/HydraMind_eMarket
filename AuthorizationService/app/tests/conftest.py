from pytest import fixture

from logic.init import init_mediator
from logic.mediator import Mediator
from infrastructure.repositories.user import BaseUsersRepository, MemoryUsersRepository


@fixture(scope='function')
def users_repository() -> MemoryUsersRepository:
    return MemoryUsersRepository()

@fixture(scope='function')
def mediator(users_repository: BaseUsersRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator, users_repository)
    return mediator