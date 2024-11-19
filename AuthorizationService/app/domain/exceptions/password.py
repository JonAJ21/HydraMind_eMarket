from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=False)
class PasswordTooLongException(ApplicationException):
    text: str
    
    @property
    def message(self):
        return f'Too long user password: "{self.text[:64]}..."'
    
    
@dataclass(eq=False)
class PasswordIsEmptyException(ApplicationException):

    @property
    def message(self):
        return 'Password is empty'