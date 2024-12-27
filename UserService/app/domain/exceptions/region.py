from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=False)
class RegionNameIsTooLongException(ApplicationException):
    text: str
    
    @property
    def message(self):
        return f'Too long region name: "{self.text[:128]}..."'
    
    