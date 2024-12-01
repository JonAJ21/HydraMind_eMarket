from dataclasses import dataclass

from logic.services.auth import BaseAuthService
from logic.exceptions.auth import UserLoginAlreadyExistsException
from infrastructure.repositories.users import BaseUsersRepository
from domain.entities.user import User
from logic.commands.base import BaseCommand, CommandHandler

@dataclass(frozen=True)
class RegisterUserCommand(BaseCommand):
    login: str
    password: str
    #role: str
    
@dataclass(frozen=True)
class RegisterUserCommandHandler(CommandHandler[RegisterUserCommand, User]):
    users_repository: BaseUsersRepository
    auth_service: BaseAuthService
    async def handle(self, command: RegisterUserCommand) -> User:
        return await self.auth_service.register(login=command.login, password=command.password)
        
        
        
            