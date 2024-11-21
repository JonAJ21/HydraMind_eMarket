from pytest import fixture

from punq import Container


from tests.fixtures import init_dummy_container
from logic.mediator import Mediator
from infrastructure.repositories.user import BaseUsersRepository, MemoryUsersRepository


@fixture(scope='function')
def container() -> Container:
    return init_dummy_container()

@fixture(scope='function')
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)

@fixture(scope='function')
def users_repository(container: Container) -> BaseUsersRepository:
    return container.resolve(BaseUsersRepository)
