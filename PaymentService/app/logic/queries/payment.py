
from dataclasses import dataclass

from logic.services.payment import BasePaymentService
from logic.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetPaymentStatusQuery(BaseQuery):
    name: str
    price: float
    
@dataclass(frozen=True)
class PaymentStatus(BaseQuery):
    status: str
    
@dataclass(frozen=True)
class GetPaymentStatusQueryHandler(QueryHandler[GetPaymentStatusQuery, PaymentStatus]):
    payment_service: BasePaymentService
   
    async def handle(self, query: GetPaymentStatusQuery) -> PaymentStatus:
        return await self.payment_service.get_payment_status(query.name, query.price)