from dataclasses import dataclass
from typing import List

from domain.entities.order import Order
from logic.services.order import BaseOrderService
from logic.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetOrderInfoQuery(BaseQuery):
    token: str
    order_id: str
    
@dataclass(frozen=True)
class GetOrderInfoQueryHandler(QueryHandler[GetOrderInfoQuery, Order]):
    order_service: BaseOrderService
   
    async def handle(self, query: GetOrderInfoQuery) -> Order:
        return await self.order_service.get_order_info(query.token, query.order_id)
    
@dataclass(frozen=True)
class GetOrdersInfoQuery(BaseQuery):
    token: str
    limit: int
    
@dataclass(frozen=True)
class GetOrdersInfoQueryHandler(QueryHandler[GetOrdersInfoQuery, List[Order]]):
    order_service: BaseOrderService
   
    async def handle(self, query: GetOrdersInfoQuery) -> List[Order]:
        return await self.order_service.get_orders_info(query.token, query.limit)