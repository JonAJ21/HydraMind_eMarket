
from dataclasses import dataclass

from logic.services.recomendation import BaseRecomendationService
from domain.entities.recomendation import Recomendation
from logic.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetRecomendationQuery(BaseQuery):
    token: str
    n_recommendations: int
    
@dataclass(frozen=True)
class GetRecomendationQueryHandler(QueryHandler[GetRecomendationQuery, Recomendation]):
    recomendation_service: BaseRecomendationService
   
    async def handle(self, query: GetRecomendationQuery) -> Recomendation:
        return await self.recomendation_service.get_recomendation(query.token, query.n_recommendations)