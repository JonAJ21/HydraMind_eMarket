from dataclasses import dataclass


from domain.exceptions.locality import LocalityNameIsTooLongException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Locality(BaseValueObject):
    value: str
    
    def validate(self):
        if len(self.value) > 128:
            raise LocalityNameIsTooLongException(self.value)
    
    def as_generic_type(self):
        return str(self.value)