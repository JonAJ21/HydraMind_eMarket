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
        
        
        # user = await self.users_repository.get_user(command.login)
        
        # if user is None:
        #     raise UserDoesNotExistException(command.login)
        # if user.password != str.encode(command.password):
        #     raise IncorrectPasswordException(command.password)
        # if not user.active:
        #     raise InactiveUserException(command.login)
    
        # # TODO: read events
    
        # jwt_payload: Dict[str, Any] = {
        #     'sub': user.login.as_generic_type(),
        #     'role': user.role.as_generic_type(),
        #     'oid': user.oid
        # }
        
        # access_jwt_payload = jwt_payload.copy()
        # refresh_jwt_payload = jwt_payload.copy()
        
        # access_jwt_payload['type'] = 'access'
        # refresh_jwt_payload['type'] = 'refresh'
        
        # access_token = JWT.encode(
        #     access_jwt_payload,
        #     expire_minutes=settings.auth_jwt.access_token_expire_minutes
        # )
        # refresh_token = JWT.encode(
        #     refresh_jwt_payload,
        #     expire_minutes=settings.auth_jwt.refresh_token_expire_minutes
        # )
           
        # return TokenInfo(
        #     access_token=access_token,
        #     refresh_token=refresh_token
        # )
        