from dataclasses import dataclass

from domain.exceptions.login import LoginIsEmptyException, LoginTooLongException
from domain.values.base import BaseValueObject



@dataclass(frozen=True)
class Login(BaseValueObject):
    value: str
    
    def validate(self):
        if len(self.value) > 52:
            raise LoginTooLongException(self.value)
        if not self.value:
            raise LoginIsEmptyException(self.value)
    
    def as_generic_type(self):
        return str(self.value)
    