from dataclasses import dataclass


from domain.exceptions.street import StreetNameIsTooLongException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Street(BaseValueObject):
    value: str
    
    def validate(self):
        if len(self.value) > 128:
            raise StreetNameIsTooLongException(self.value)
    
    def as_generic_type(self):
        return str(self.value)