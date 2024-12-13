
from dataclasses import dataclass

from domain.entities.storage import Storage
from domain.entities.product import Product
from domain.entities.base import BaseEntity


@dataclass
class ProductStorageCount(BaseEntity):
    product_id: str | None
    storage_id: str | None
    count: int | None

    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'ProductStorageCount') -> bool:
        return self.oid == __value.oid
    
@dataclass    
class ProductStorage(BaseEntity):
    product: Product
    storage: Storage
    psc: ProductStorageCount
    
    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'ProductStorage') -> bool:
        return self.oid == __value.oid