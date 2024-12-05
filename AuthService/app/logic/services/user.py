from abc import ABC, abstractmethod
from dataclasses import dataclass

from logic.exceptions.auth import InvalidTokenTypeException, UserDoesNotExistException
from logic.services.jwt import JWT
from infrastructure.repositories.users import BaseUsersRepository
from domain.entities.user import User


@dataclass
class BaseUserService(ABC):
    
    @abstractmethod
    async def get_user_by_token(self, token: str, token_type: str) -> User:
        ...
        
@dataclass
class JWTUserService(BaseUserService):
    users_repository: BaseUsersRepository
    
    async def get_user_by_token(self, token: str, token_type: str) -> User:
        if token_type not in ['access', 'refresh']:
            raise InvalidTokenTypeException(token_type)
        
        payload: dict = JWT.decode(
            token=token
        )
        
        payload_token_type = payload.get('type')
        if payload_token_type != token_type:
            raise InvalidTokenTypeException(payload_token_type)
        
        login: str | None = payload.get('sub')

        user: User | None = await self.users_repository.get_user(login)
        
        if not user:
            raise UserDoesNotExistException(login)
        
        return user
        
        