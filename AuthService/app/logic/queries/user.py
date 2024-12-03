from dataclasses import dataclass
from typing import Any

from logic.services.user import BaseUserService
from logic.queries.base import BaseQuery, QueryHandler
#from infrastructure.repositories.users import BaseUsersRepository
from domain.entities.user import User

@dataclass(frozen=True)
class GetUserInfoQuery(BaseQuery):
    token: str
    
@dataclass(frozen=True)
class GetUserInfoQueryHandler(QueryHandler[GetUserInfoQuery, User]):
    users_service: BaseUserService
    
    async def handle(self, query: GetUserInfoQuery) -> User:
        return await self.users_service.get_user_by_token(query.token, 'access')