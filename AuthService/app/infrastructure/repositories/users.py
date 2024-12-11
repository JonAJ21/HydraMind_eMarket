from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from asyncpg import Pool, create_pool

from domain.values.email import Email
from domain.values.role import Role
from domain.values.password import Password
from domain.values.login import Login
from domain.entities.user import User
from settings.config import settings


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



# @dataclass
# class PostgreSQLPool:
#     _pool: Pool | None = None
    
#     async def init_pool(self):
#         self._pool = await create_pool(
#             user=settings.postgre_sql.user,
#             password=settings.postgre_sql.password,
#             database=settings.postgre_sql.db_name,
#             host=settings.postgre_sql.db_host,
#             port=settings.postgre_sql.db_port,
#             min_size=settings.postgre_sql.pool_min_size,
#             max_size=settings.postgre_sql.pool_max_size
#         )
        
#     async def __aenter__(self):
#         return await self.init_pool()
    
#     async def __aexit__(self):
#         await self._pool.close()
       
@dataclass
class PostgreUsersRepository(BaseUsersRepository):
    _connection_pool: Pool = settings.postgre_sql_pool.pool
    
   
    async def get_user(self, login: str) -> User | None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT user_id, login, password, email, role, active
                    FROM users 
                    WHERE login = $1           
                '''
                
                row = await connection.fetchrow(
                    query,
                    login
                )
                if row is not None:
                    if row['email'] is None:
                        user = User(
                            oid=str(row['user_id']),
                            login=Login(row['login']),
                            password=Password(bytes(row['password'], 'utf-8')),
                            email=None,
                            role=Role(row['role']),
                            active=row['active']
                        )
                    else:
                        user = User(
                            oid=str(row['user_id']),
                            login=Login(row['login']),
                            password=Password(bytes(row['password'], 'utf-8')),
                            email=Email(row['email']),
                            role=Role(row['role']),
                            active=row['active']
                        )
                        
                    return user
        return None
    
    
    async def register_user(self, user: User) -> None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                
                query = '''  
                    INSERT INTO users 
                        (user_id, login, password, role, active) 
                        VALUES
                        ($1, $2, $3, $4, $5);
                    '''
                
                await connection.execute(
                    query,
                    user.oid,
                    user.login.as_generic_type(),
                    user.password.as_generic_type(),
                    user.role.as_generic_type(),
                    user.active
                )
                
                
                
                
        
        
    
        
