from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict

from domain.entities.user import User
from settings.config import settings
from logic.exceptions.auth import InactiveUserException, IncorrectPasswordException, InvalidTokenTypeException, UserDoesNotExistException, UserLoginAlreadyExistsException
from infrastructure.repositories.users import BaseUsersRepository
from logic.services.jwt import JWT, TokenInfo

@dataclass
class BaseAuthService(ABC):
    
    @abstractmethod
    async def register(self, login: str, password: str) -> User:
        ...
    
    @abstractmethod
    async def login(self, login: str, password: str) -> TokenInfo:
        ...

    # @abstractmethod
    # async def get_user_by_token(self, token: str) -> User:
    #     ...
        
        
@dataclass
class JWTAuthService(BaseAuthService):
    users_repository: BaseUsersRepository
    
    async def register(self, login: str, password: str) -> User:
        if await self.users_repository.get_user(login) is not None:
            raise UserLoginAlreadyExistsException(login)
        
        user = User.register_user(
            login=login,
            password=password,
            role='CUSTOMER'
        )
        
        # TODO: read events
        
        await self.users_repository.register_user(user)
        
        return user
    
    async def login(self, login: str, password: str) -> TokenInfo:
        user = await self.users_repository.get_user(login)
        
        if user is None:
            raise UserDoesNotExistException(login)
        if user.password != str.encode(password):
            raise IncorrectPasswordException(password)
        if not user.active:
            raise InactiveUserException(login)
        
        #TODO read events
        
        jwt_payload: Dict[str, Any] = {
            'sub': user.login.as_generic_type(),
            'role': user.role.as_generic_type(),
            'oid': user.oid
        }
        
        access_jwt_payload = jwt_payload.copy()
        refresh_jwt_payload = jwt_payload.copy()
        
        access_jwt_payload['type'] = 'access'
        refresh_jwt_payload['type'] = 'refresh'
        
        access_token = JWT.encode(
            access_jwt_payload,
            expire_minutes=settings.auth_jwt.access_token_expire_minutes
        )
        refresh_token = JWT.encode(
            refresh_jwt_payload,
            expire_minutes=settings.auth_jwt.refresh_token_expire_minutes
        )
           
        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    # async def get_user_by_token(self, token: str) -> User:
    #     payload: dict = JWT.decode(
    #         token=token
    #     )
    #     token_type = payload.get('type')
    #     if token_type != 'access':
    #         raise InvalidTokenTypeException(token_type)
        
    #     login: str | None = payload.get('sub')

    #     user: User | None = await self.users_repository.get_user(login)
        
    #     if not user:
    #         raise UserDoesNotExistException(login)
        
    #     return user