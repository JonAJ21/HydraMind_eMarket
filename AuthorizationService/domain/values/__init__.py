from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

VT = TypeVar('VT', bound=Any)

@dataclass(frozen=True)
class BaseValueObject(ABC, Generic[VT]):
    value: VT

    @abstractmethod
    def validate(self):
        ...
    
    @abstractmethod
    def as_generic_type(self):
        ...