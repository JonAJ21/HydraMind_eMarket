from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=False)
class BuildingNameIsTooLongException(ApplicationException):
    text: str
    
    @property
    def message(self):
        return f'Too long building name: "{self.text[:16]}..."'