

from dataclasses import dataclass
from typing import List

from domain.entities.category import Category
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

@dataclass(frozen=True)
class GetCategoriesQuery(BaseQuery):
    ...
    
@dataclass(frozen=True)
class GetCategoriesQueryHandler(QueryHandler[GetCategoriesQuery, List[Category]]):
    catalog_service: BaseCatalogService
   
    async def handle(self, query: GetCategoriesQuery) -> List[Category]:
        return await self.catalog_service.get_categories()
  
