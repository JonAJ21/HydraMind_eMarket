from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from domain.entities.product import Product
from domain.entities.base import BaseEntity


@dataclass
class Order(BaseEntity):
    user_id: str
    status: str
    
    is_paid: bool = False
    time_created: datetime = datetime.now()
    
    time_delivered: datetime | None = None
    
    products: List[Product] = field(
        default_factory=list,
        kw_only=True
    )
    
    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'Order') -> bool:
        return self.oid == __value.oid
    
@dataclass
class OrderProductCount(BaseEntity):
    order_id: str
    product_id: str
    count: int

