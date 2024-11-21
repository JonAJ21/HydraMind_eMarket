import pytest

from punq import Container

from logic.exceptions.user import UserWithThatEmailAlreadyExistsException
from domain.values.email import Email
from domain.values.password import Password
from domain.values.role import Role
from domain.values.login import Login
from domain.entities.user import User
from logic.commands.user import AddUserCommand
from logic.mediator import Mediator
from infrastructure.repositories.user import BaseUsersRepository

@pytest.mark.asyncio
async def test_add_user_command_succes(
    users_repository: BaseUsersRepository,
    mediator: Mediator
):    
    
    # TODO: faker for random text generation
    user, *_ = await mediator.handle_command(
        AddUserCommand(
            login='login', password='password',
            email='email', role="CUSTOMER"
    ))
    
    assert await users_repository.check_user_exists_by_email(email=user.email.as_generic_type())
    assert await (users_repository.check_user_exists_by_email(email='emai')) == False
    


@pytest.mark.asyncio
async def test_add_user_command_email_already_exists(
    users_repository: BaseUsersRepository,
    mediator: Mediator
):
    # TODO: faker for random text generation
    
    user = User(login=Login('login2'),
                password=Password('password2'),
                email=Email('email2'),
                role=Role('CUSTOMER'))
    
    await users_repository.add_user(user)
    
    with pytest.raises(UserWithThatEmailAlreadyExistsException):
        await mediator.handle_command(
            AddUserCommand(
                login=user.login.as_generic_type(),
                password=user.password.as_generic_type(),
                email=user.email.as_generic_type(),
                role=user.role.as_generic_type()                                   
        ))
        
    assert len(users_repository._saved_users) == 1