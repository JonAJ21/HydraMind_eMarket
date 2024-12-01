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
        return f'Incorrect password: {self.password}'

@dataclass(eq=False)    
class InactiveUserException(LogicException):
    login: str
    
    @property
    def message(self):
        return f'{self.login} is inactive user'
        
@dataclass(eq=False)    
class InvalidTokenTypeException(LogicException):
    token_type: str
    
    @property
    def message(self):
        if self.token_type == 'access':
            return f'Invalid token type "{self.token_type}" expected "refresh"'
        if self.token_type == 'refresh':
            return f'Invalid token type "{self.token_type}" expected "access"'
        
        return f'Invalid token type "{self.token_type}". It must be "access" or "refresh"'
    