from dataclasses import dataclass
from typing import Any

from logic.jwt import JWT
from logic.queries.base import BaseQuery, QueryHandler
from logic.exceptions.auth import UserDoesNotExistException, UserLoginAlreadyExistsException
from infrastructure.repositories.users import BaseUsersRepository
from domain.entities.user import User

@dataclass(frozen=True)
class GetUserInfoQuery(BaseQuery):
    token: str
    
@dataclass(frozen=True)
class GetUserInfoQueryHandler(QueryHandler[GetUserInfoQuery, User]):
    users_repository: BaseUsersRepository
    
    async def handle(self, query: GetUserInfoQuery) -> User:
        payload: dict = JWT.decode(
            token=query.token
        )
        print(query.token)
        login: str | None = payload.get('sub')
        
        user: User | None = await self.users_repository.get_user(login)
        
        if not user:
            raise UserDoesNotExistException(query.login)
        
        return user