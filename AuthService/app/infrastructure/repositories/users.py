from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from domain.entities.user import User

@dataclass
class BaseUsersRepository(ABC):
    @abstractmethod
    async def get_user(self, login: str) -> User | None:
        ...
        
    @abstractmethod
    async def register_user(self, user: User) -> None:
        ...
        
        
@dataclass
class MemoryUsersRepository(BaseUsersRepository):
    _saved_users: list[User] = field(
        default_factory=list,
        kw_only=True
    )
        
    async def get_user(self, login: str) -> User | None:
        for user in self._saved_users:
            if user.login.as_generic_type() == login:
                return user
        return None
        
    async def register_user(self, user: User) -> None:
        self._saved_users.append(user)
        
@dataclass
class PostgreUsersRepository(BaseUsersRepository):
    ...