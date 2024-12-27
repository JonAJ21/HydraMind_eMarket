from dataclasses import dataclass
from typing import List

from logic.services.storage import BaseStorageService
from domain.entities.product_storage_count import ProductStorage
from logic.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetProductsInfoBySalesmanQuery(BaseQuery):
    token: str
    
@dataclass(frozen=True)
class GetProductsInfoBySalesmanQueryHandler(QueryHandler[GetProductsInfoBySalesmanQuery, List[ProductStorage]]):
    storage_service: BaseStorageService
   
    async def handle(self, query: GetProductsInfoBySalesmanQuery) -> List[ProductStorage]:
        # print(query.token)
        # print()
        return await self.storage_service.get_products_info_by_salesman(query.token)