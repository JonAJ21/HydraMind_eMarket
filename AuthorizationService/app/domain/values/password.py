from dataclasses import dataclass

from domain.exceptions.password import PasswordIsEmptyException, PasswordTooLongException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Password(BaseValueObject):
    value: str
    
    def validate(self):
        if len(self.value) > 64:
            raise PasswordTooLongException(self.value)
        if not self.value:
            raise PasswordIsEmptyException(self.value)
    
    def as_generic_type(self):
        return str(self.value)
    