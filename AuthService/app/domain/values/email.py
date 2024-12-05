from dataclasses import dataclass

from domain.exceptions.email import EmailIsEmptyException, EmailTooLongException
from domain.values.base import BaseValueObject



@dataclass(frozen=True)
class Email(BaseValueObject):
    value: str
    
    def validate(self):
        # TODO: validation isEmail?
        if len(self.value) > 128:
            raise EmailTooLongException(self.value)
        if not self.value:
            raise EmailIsEmptyException(self.value)
    
    def as_generic_type(self):
        return str(self.value)