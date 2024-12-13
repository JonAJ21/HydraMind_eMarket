
from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass
class Storage(BaseEntity):
    region: str | None
    locality: str | None
    street: str | None
    building: str | None

    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'Storage') -> bool:
        return self.oid == __value.oid