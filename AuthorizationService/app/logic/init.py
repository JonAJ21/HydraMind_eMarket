from infrastructure.repositories.user import BaseUsersRepository, MemoryUsersRepository
from logic.commands.user import AddUserCommand, AddUserCommandHandler
from logic.mediator import Mediator


def init_mediator(mediator: Mediator,
                  users_repository: BaseUsersRepository):
    mediator.register_command(
        AddUserCommand,
        [AddUserCommandHandler(users_repository=users_repository)]
    )