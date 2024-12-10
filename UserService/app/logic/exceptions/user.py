
from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class BadRequestToAuthServiceException(LogicException):
    
    @property
    def message(self):
        return f'Bad request to auth service'