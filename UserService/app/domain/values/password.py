from dataclasses import dataclass

from domain.values.base import BaseValueObject

@dataclass(frozen=True)
class Password(BaseValueObject):
    value: bytes
    
    def validate(self):
        ...
    
    def as_generic_type(self):
        return self.value.decode(encoding='utf-8')