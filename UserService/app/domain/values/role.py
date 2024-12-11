from dataclasses import dataclass

from domain.exceptions.role import RoleIsIncorrectException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Role(BaseValueObject):
    value: str
    
    def validate(self):
        roles = ['CUSTOMER', 'SALESMAN', 'ADMIN']
        if self.value not in roles:
            raise RoleIsIncorrectException(self.value)
    
    def as_generic_type(self):
        return str(self.value)