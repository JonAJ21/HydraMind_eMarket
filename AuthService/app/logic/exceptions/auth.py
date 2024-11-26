from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class UserLoginAlreadyExistsException(LogicException):
    login: str

    @property
    def message(self):
        return f'User with login {self.login} already exists'