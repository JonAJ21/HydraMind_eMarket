from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=False)
class EmailTooLongException(ApplicationException):
    text: str
    
    @property
    def message(self):
        return f'Too long user email: "{self.text[:128]}..."'
    


@dataclass(eq=False)
class EmailIsEmptyException(ApplicationException):

    @property
    def message(self):
        return 'Email is empty'