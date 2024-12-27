
from dataclasses import dataclass, field
from typing import List

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class BadRequestToAuthServiceException(LogicException):
    
    @property
    def message(self):
        return f'Bad request to auth service'
    
@dataclass(eq=False)
class PermissionDeniedException(LogicException):
    valid_roles: List[str] = field(
        default_factory=list,
        kw_only=True
    )
    role: str
    
    @property
    def message(self):
        return f'Permission denied your role must be in {self.valid_roles}. Your role is {self.role}'