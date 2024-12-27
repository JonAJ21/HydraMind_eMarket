from dataclasses import dataclass
from typing import List
from datetime import datetime
from domain.entities.base import BaseEntity

@dataclass
class Recomendation(BaseEntity):
    user_id: str
    recommended_products: List[str]
    generated_at: datetime = datetime.now()

    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'Recomendation') -> bool:
        return self.oid == __value.oid
    
    