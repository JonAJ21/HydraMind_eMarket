from dataclasses import dataclass

from logic.exceptions.base import LogicException

@dataclass
class CategoryDoesNotExistException(LogicException):
    category_name: str
    
    @property
    def message(self):
        return f'Category does not exists: {self.category_name}'
    
@dataclass
class CategoryWithNameAlreadyExistsException(LogicException):
    category_name: str
    
    @property
    def message(self):
        return f'Category with name {self.category_name} already exists'