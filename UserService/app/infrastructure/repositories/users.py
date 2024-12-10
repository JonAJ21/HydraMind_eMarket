from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from asyncpg import Pool


from domain.values.login import Login
from domain.values.password import Password
from domain.values.role import Role
from domain.entities.adress import Adress
from domain.entities.user import User
from settings.config import settings


@dataclass
class BaseUsersRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> User | None:
        ...
        
    @abstractmethod
    async def change_user_email(self, user_id: str, new_email: str) -> bool:
        ...

    @abstractmethod
    async def add_user_adress(
        self, user_id: str, region: str, 
        locality: str, street: str, building: str) -> Adress:
        ...
    
    # @abstractmethod
    # async def get_user_adresses(self, user_id: str) -> List[Adress]:
    #     ...
    
    # @abstractmethod
    # async def delete_user_adress(self, user_id: str, adress_id: str) -> None:
    #     ...
        
    # @abstractmethod
    # async def deactivate_user_by_login(self, admin_id: str, login: str) -> None:
    #     ...
    
    # @abstractmethod
    # async def activate_user_by_login(self, admin_id: str, login: str) -> None:
    #     ...
    
    # @abstractmethod
    # async def change_role(self, admin_id: str, new_role: str) -> None:
    #     ...
    
    


@dataclass
class PostgreUsersRepository(BaseUsersRepository):
    _connection_pool: Pool = settings.postgre_sql_pool.pool
    
    async def get_user_by_id(self, user_id: str) -> User:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT user_id, login, password, email, role, active
                    FROM users                      
                    WHERE user_id = $1;
                '''
                
                row = await connection.fetchrow(
                    query,
                    user_id
                )
                
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
                        email=row['email'],
                        role=Role(row['role']),
                        active=row['active']
                    )
                return user
    
    
    async def change_user_email(self, user_id, new_email) -> bool:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    UPDATE users
                        SET email = $1
                    WHERE user_id = $2;
                '''
                
                await connection.execute(query, new_email, user_id)
        return True
        
    async def add_user_adress(self, user_id, region, locality, street, building) -> Adress:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    INSERT INTO users_adresses
                        (user_adress_id, user_id, region, locality, street, building)
                    VALUES ($1, $2, $3, $4, $5, $6);
                '''
                adress = Adress.add_address(user_id, region, locality, street, building)
                
                
                await connection.execute(query, adress.oid, user_id, region, locality, street, building)
        
        return adress
       
    

                
                
                
                
        
        
    
        
