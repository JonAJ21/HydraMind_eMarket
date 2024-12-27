

from dataclasses import dataclass

from logic.services.user import BaseUserService
from domain.entities.user import User
from logic.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetUserInfoQuery(BaseQuery):
    token: str
    
@dataclass(frozen=True)
class GetUserInfoQueryHandler(QueryHandler[GetUserInfoQuery, User]):
    users_service: BaseUserService
    
    async def handle(self, query: GetUserInfoQuery) -> User:
        return await self.users_service.get_user(query.token)
    
    