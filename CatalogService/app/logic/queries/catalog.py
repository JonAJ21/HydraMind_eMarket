

from dataclasses import dataclass
from typing import List

from logic.services.catalog import BaseCatalogService
from domain.entities.product import Product
from logic.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetProductsByCategoryQuery(BaseQuery):
    category_name: str
    
@dataclass(frozen=True)
class GetProductsByCategoryQueryHandler(QueryHandler[GetProductsByCategoryQuery, List[Product]]):
    catalog_service: BaseCatalogService
   
    async def handle(self, query: GetProductsByCategoryQuery) -> List[Product]:
        return await self.catalog_service.get_products_by_category(query.category_name)