from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=False)
class StreetNameIsTooLongException(ApplicationException):
    text: str
    
    @property
    def message(self):
        return f'Too long street name: "{self.text[:128]}..."'