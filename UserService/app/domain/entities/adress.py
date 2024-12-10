from dataclasses import dataclass

from domain.values.building import Building
from domain.entities.base import BaseEntity
from domain.values.locality import Locality
from domain.values.region import Region
from domain.values.street import Street


@dataclass
class Adress(BaseEntity):
    user_id: str
    region: Region
    locality: Locality
    street: Street
    building: Building
    
    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'Adress') -> bool:
        return self.oid == __value.oid
    
    @classmethod
    def add_address(
        cls, 
        user_id: str,
        region: str,
        locality: str,
        street: str,
        building: str,
    ) -> 'Adress':        
        
        return Adress(
            user_id=user_id,
            region=Region(region),
            locality=Locality(locality),
            street=Street(street),
            building=Building(building)
        )
    