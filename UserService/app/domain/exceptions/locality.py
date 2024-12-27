from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=False)
class LocalityNameIsTooLongException(ApplicationException):
    text: str
    
    @property
    def message(self):
        return f'Too long locality name: "{self.text[:128]}..."'