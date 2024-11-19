from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=False)
class LoginTooLongException(ApplicationException):
    text: str
    
    @property
    def message(self):
        return f'Too long user login: "{self.text[:52]}..."'
    
    
@dataclass(eq=False)
class LoginIsEmptyException(ApplicationException):

    @property
    def message(self):
        return 'Login is empty'