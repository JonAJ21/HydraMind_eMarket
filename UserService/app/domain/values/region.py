from dataclasses import dataclass


from domain.exceptions.region import RegionNameIsTooLongException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Region(BaseValueObject):
    value: str
    
    def validate(self):
        if len(self.value) > 128:
            raise RegionNameIsTooLongException(self.value)
    
    def as_generic_type(self):
        return str(self.value)