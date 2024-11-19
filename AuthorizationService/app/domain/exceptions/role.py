from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=False)
class RoleIsIncorrectException(ApplicationException):
    text: str
    
    @property
    def message(self):
        return f'Role is incorrect: {self.text}'
    
