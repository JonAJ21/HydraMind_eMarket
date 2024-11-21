from dataclasses import dataclass

from logic.exceptions.base import LogicException

@dataclass(eq=False)
class UserWithThatEmailAlreadyExistsException(LogicException):
    email: str
    
    @property
    def message(self):
        return f'User with that email already exists: {self.email}'