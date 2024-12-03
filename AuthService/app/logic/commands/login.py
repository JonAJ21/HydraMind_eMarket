from dataclasses import dataclass
from typing import Any, Dict

from logic.services.auth import BaseAuthService
from settings.config import settings
from logic.services.jwt import TokenInfo
from logic.exceptions.auth import InactiveUserException, IncorrectPasswordException, UserDoesNotExistException
from infrastructure.repositories.users import BaseUsersRepository
from domain.entities.user import User
from logic.commands.base import BaseCommand, CommandHandler

@dataclass(frozen=True)
class LoginUserCommand(BaseCommand):
    login: str
    password: str
    
@dataclass(frozen=True)
class LoginUserCommandHandler(CommandHandler[LoginUserCommand, TokenInfo]):
    users_repository: BaseUsersRepository

    auth_service: BaseAuthService    
    async def handle(self, command: LoginUserCommand) -> TokenInfo:
        return await self.auth_service.login(login=command.login, password=command.password)
        