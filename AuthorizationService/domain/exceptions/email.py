from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=False)
class UserEmailTooLongException(ApplicationException):
    text: str
    
    @property
    def message(self):
        return f'Too long user email: "{self.text[:255]}..."'
    


@dataclass(eq=False)
class UserEmailIsEmptyException(ApplicationException):

    @property
    def message(self):
        return 'Email is empty'