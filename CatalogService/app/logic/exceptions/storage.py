from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class StorageDoesNotExistException(LogicException):

    @property
    def message(self):
        return f'Storage does not exists'
    
@dataclass
class StorageAlreadyExistsException(LogicException):
    
    @property
    def message(self):
        return f'Storage already exists'
    
@dataclass
class NoProductInStorageException(LogicException):
    
    @property
    def message(self):
        return f'No product in storage'
    
@dataclass
class NotEnoughProductInStorageException(LogicException):
    count_in_storage: int
    
    @property
    def message(self):
        return f'Not enough product in storage exception. Product count in storage: {self.count_in_storage}'