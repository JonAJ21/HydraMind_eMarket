
from dataclasses import dataclass
from typing import List

from logic.queries.base import BaseQuery
from logic.queries.base import QueryHandler
from domain.entities.adress import Adress
from logic.services.user import BaseUserService


@dataclass(frozen=True)
class GetAdressesQuery(BaseQuery):
    token: str
    
@dataclass(frozen=True)
class GetAdressesQueryHandler(QueryHandler[GetAdressesQuery, List[Adress]]):
    user_service: BaseUserService
   
    async def handle(self, query: GetAdressesQuery) -> List[Adress]:
        return await self.user_service.get_user_adresses(query.token)