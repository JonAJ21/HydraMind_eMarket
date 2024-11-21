from dataclasses import dataclass

from domain.entities.user import User
from infrastructure.repositories.user import BaseUsersRepository
from domain.values.role import Role
from domain.values.email import Email
from domain.values.password import Password
from domain.values.login import Login
from logic.exceptions.user import UserWithThatEmailAlreadyExistsException
from logic.commands.base import BaseCommand, CommandHandler

@dataclass(frozen=True)
class AddUserCommand(BaseCommand):
    login: str
    password: str
    email: str
    role: str
    
    
@dataclass(frozen=True)
class AddUserCommandHandler(CommandHandler[AddUserCommand, User]):
    users_repository: BaseUsersRepository
    
    async def handle(self, command: AddUserCommand) -> User:
        if await self.users_repository.check_user_exists_by_email(command.email):
            raise UserWithThatEmailAlreadyExistsException(command.email)
        
        login = Login(value=command.login)
        password = Password(value=command.password)
        email = Email(value=command.email)
        role = Role(value=command.role)
        
        # TODO : read events
        
        new_user = User.add_user(login=login, password=password, email=email, role=role)
        await self.users_repository.add_user(new_user)
        
        return new_user
        
        
        
    