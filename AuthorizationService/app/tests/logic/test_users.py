import pytest

from logic.commands.user import AddUserCommand
from logic.mediator import Mediator
from infrastructure.repositories.user import BaseUsersRepository

@pytest.mark.asyncio
async def test_add_user_command_succes(
    users_repository: BaseUsersRepository,
    mediator: Mediator,
):
    # TODO: faker for random text generation
    user = (await mediator.handle_command(
        AddUserCommand(
            login='login', password='password',
            email='email', role="CONSUMER"
    )))[0]
    assert users_repository.check_users_exists_by_email(email=user.email.as_generic_type())
    
    