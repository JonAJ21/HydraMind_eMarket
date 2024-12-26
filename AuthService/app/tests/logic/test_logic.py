import pytest
from unittest.mock import AsyncMock
from logic.commands.register import RegisterUserCommand, RegisterUserCommandHandler
from domain.entities.user import User
from logic.services.auth import BaseAuthService
from infrastructure.repositories.users import BaseUsersRepository

@pytest.mark.asyncio
async def test_register_user_command_handler():
    users_repository = AsyncMock(BaseUsersRepository)
    auth_service = AsyncMock(BaseAuthService)
    
    command = RegisterUserCommand(login="test_user", password="test_password")
    user = User.register_user(login="test_user", password="hashed_password")
    
    auth_service.register = AsyncMock(return_value=user)
    
    handler = RegisterUserCommandHandler(
        users_repository=users_repository,
        auth_service=auth_service
    )
    
    result = await handler.handle(command)
    
    assert result == user
    auth_service.register.assert_called_once_with(
        login="test_user",
        password="test_password"
    )
