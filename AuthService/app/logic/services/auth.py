from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict

from logic.services.user import BaseUserService
from domain.entities.user import User
from settings.config import settings
from logic.exceptions.auth import InactiveUserException, IncorrectPasswordException, InvalidTokenTypeException, UserDoesNotExistException, UserLoginAlreadyExistsException
from infrastructure.repositories.users import BaseUsersRepository
from logic.services.jwt import JWT, TokenInfo

@dataclass
class BaseAuthService(ABC):
    
    @abstractmethod
    async def validate_auth(self, login: str, password: str) -> User:
        ...
    
    @abstractmethod
    async def register(self, login: str, password: str) -> User:
        ...
    
    @abstractmethod
    async def create_token(self, user: User, token_type: str) -> str:
        ...
    
    @abstractmethod
    async def login(self, login: str, password: str) -> TokenInfo:
        ...
    
    @abstractmethod
    async def refresh(self, token: str) -> TokenInfo:
        ...
        
        
@dataclass
class JWTAuthService(BaseAuthService):
    users_repository: BaseUsersRepository
    users_service: BaseUserService
    
    async def validate_auth(self, login: str, password: str) -> User:
        user = await self.users_repository.get_user(login)
        
        if user is None:
            raise UserDoesNotExistException(login)
        if user.password != str.encode(password):
            raise IncorrectPasswordException(password)
        if not user.active:
            raise InactiveUserException(login)
        
        return user
        
    
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
    
    
    async def create_token(self, user: User, token_type: str) -> str:
        if token_type not in ['access', 'refresh']:
            raise InvalidTokenTypeException(token_type=token_type)
        
        jwt_payload: Dict[str, Any] = {
            'sub': user.login.as_generic_type(),
            'role': user.role.as_generic_type(),
            'oid': user.oid
        }
        
        jwt_payload = jwt_payload.copy()
        jwt_payload['type'] = token_type
        
        if token_type == 'access':
            return JWT.encode(
                jwt_payload,
                expire_minutes=settings.auth_jwt.access_token_expire_minutes
            ) 
        return JWT.encode(
            jwt_payload,
            expire_minutes=settings.auth_jwt.refresh_token_expire_minutes
        )
    
    
    async def login(self, login: str, password: str) -> TokenInfo:
        
        user = await self.validate_auth(login=login, password=password)    
        
        #TODO read events
           
        return TokenInfo(
            access_token=await self.create_token(user=user, token_type='access'),
            refresh_token=await self.create_token(user=user, token_type='refresh')
        )
        
    async def refresh(self, token: str) -> TokenInfo:
        user = await self.users_service.get_user_by_token(token=token, token_type='refresh')
        
        return TokenInfo(
            access_token=await self.create_token(user=user, token_type='access')
        )
        
        
        
            