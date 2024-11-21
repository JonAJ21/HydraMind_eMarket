from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from domain.entities.user import User

@dataclass
class BaseUsersRepository(ABC):
    @abstractmethod
    def check_user_exists_by_email(self, email: str) -> bool:
        ...
        
    @abstractmethod
    def add_user(self, user: User) -> None:
        ...
        
        
@dataclass
class MemoryUsersRepository(ABC):
    _saved_users: list[User] = field(
        default_factory=list,
        kw_only=True
    )
    
    def check_user_exists_by_email(self, email: str) -> bool:
        try:
            return bool(next(
                user for user in self._saved_users if user.email == email
            ))
        except StopIteration:
            return False
        
    def add_user(self, user: User) -> None:
        self._saved_users.append(user)