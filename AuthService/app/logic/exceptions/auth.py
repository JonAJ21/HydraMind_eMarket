from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class UserLoginAlreadyExistsException(LogicException):
    login: str

    @property
    def message(self):
        return f'User with login {self.login} already exists'
    
@dataclass(eq=False)
class UserDoesNotExistException(LogicException):
    login: str
    
    @property
    def message(self):
        return f'User with login {self.login} does not exist'

@dataclass(eq=False)
class IncorrectPasswordException(LogicException):
    password: str
    
    @property
    def message(self):
        f'Incorrect password: {self.password}'

@dataclass(eq=False)    
class InactiveUserException(LogicException):
    login: str
    
    @property
    def message(self):
        f'{self.password} is inactive user'