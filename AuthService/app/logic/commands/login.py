from dataclasses import dataclass
from typing import Any, Dict

from logic.jwt import JWT, TokenInfo
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
    
    async def handle(self, command: LoginUserCommand) -> TokenInfo:
        user = await self.users_repository.get_user(command.login)
        
        if user is None:
            raise UserDoesNotExistException(command.login)
        if user.password != str.encode(command.password):
            raise IncorrectPasswordException(command.password)
        if not user.active:
            raise InactiveUserException(command.login)
    
        # TODO: read events
    
        jwt_payload: Dict[str, Any] = {
            'sub': user.login.as_generic_type(),
            'role': user.role.as_generic_type(),
            'oid': user.oid
        }
        
        token = JWT.encode(jwt_payload)
        return TokenInfo(
            access_token=token,
            token_type='Bearer'
        )
        