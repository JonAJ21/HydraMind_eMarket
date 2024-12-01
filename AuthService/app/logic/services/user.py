from abc import ABC, abstractmethod
from dataclasses import dataclass

from logic.exceptions.auth import InvalidTokenTypeException, UserDoesNotExistException
from logic.services.jwt import JWT
from infrastructure.repositories.users import BaseUsersRepository
from domain.entities.user import User


@dataclass
class BaseUserService(ABC):
    
    @abstractmethod
    async def get_user_by_token(self, token: str) -> User:
        ...
        
@dataclass
class JWTUserService(BaseUserService):
    users_repository: BaseUsersRepository
    async def get_user_by_token(self, token) -> User:
        payload: dict = JWT.decode(
            token=token
        )
        token_type = payload.get('type')
        if token_type != 'access':
            raise InvalidTokenTypeException(token_type)
        
        login: str | None = payload.get('sub')

        user: User | None = await self.users_repository.get_user(login)
        
        if not user:
            raise UserDoesNotExistException(login)
        
        return user