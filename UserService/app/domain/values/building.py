from dataclasses import dataclass


from domain.exceptions.building import BuildingNameIsTooLongException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Building(BaseValueObject):
    value: str
    
    def validate(self):
        if len(self.value) > 16:
            raise BuildingNameIsTooLongException(self.value)
    
    def as_generic_type(self):
        return str(self.value)