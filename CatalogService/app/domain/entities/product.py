
from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass
class Product(BaseEntity):
    name: str
    salesman_id: str
    category_id: str
    description: str
    price: float
    discount_percent: float
    rating: float | None = None
    
    count: int = 1
    
    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'Product') -> bool:
        return self.oid == __value.oid