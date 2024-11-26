from dataclasses import dataclass

from logic.exceptions.auth import UserLoginAlreadyExistsException
from infrastructure.repositories.users import BaseUsersRepository
from domain.entities.user import User
from logic.commands.base import BaseCommand, CommandHandler

@dataclass(frozen=True)
class RegisterUserCommand(BaseCommand):
    login: str
    password: str
    role: str
    
@dataclass(frozen=True)
class RegisterUserCommandHandler(CommandHandler[RegisterUserCommand, User]):
    users_repository: BaseUsersRepository
    
    async def handle(self, command: RegisterUserCommand) -> User:
        if await self.users_repository.check_user_exists_by_login(command.login):
            raise UserLoginAlreadyExistsException(command.login)
        
        user = User.register_user(
            login=command.login,
            password=command.password,
            role=command.role
        )
        
        # TODO: read events
        
        await self.users_repository.register_user(user)
        
        return user
        
        
        
            