from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import httpx

from infrastructure.repositories.users import BaseUsersRepository
from logic.exceptions.user import BadRequestToAuthServiceException
from domain.entities.adress import Adress
from domain.entities.user import User
from settings.config import settings

@dataclass
class BaseUserService(ABC):
    
    @abstractmethod
    async def get_user(self, token: str) -> User:
        ...
        
    @abstractmethod
    async def change_email(self, token: str, new_email: str) -> bool:
        ...
        
    @abstractmethod
    async def add_user_adress(
        self, token: str, region: str,
        locality: str, street: str, building: str
    ) -> Adress:
        ...
    
    @abstractmethod
    async def get_user_adresses(self, token: str) -> List[Adress]:
        ...
    
    # @abstractmethod
    # async def delete_user_adress(self, token: str, adress_id: str) -> None:
    #     ...
        
    # @abstractmethod
    # async def deactivate_user_by_login(self, token: str, login: str) -> None:
    #     ...
    
    # @abstractmethod
    # async def activate_user_by_login(self, token: str, login: str) -> None:
    #     ...
    
    # @abstractmethod
    # async def change_role(self, token: str, new_role: str) -> None:
        ...
        
    
@dataclass
class RESTUserService(BaseUserService):
    users_repository: BaseUsersRepository 
    
    async def get_user(self, token) -> User:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        
        user_id = response.json()['oid']
        
        return await self.users_repository.get_user_by_id(user_id)
        
    async def change_email(self, token, new_email):
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        user_id = response.json()['oid']
        
        return await self.users_repository.change_user_email(user_id, new_email)

    async def add_user_adress(self, token, region, locality, street, building) -> Adress:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        user_id = response.json()['oid']
        
        return await self.users_repository.add_user_adress(
            user_id, region, locality, street, building
        )
        
    async def get_user_adresses(self, token):
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        user_id = response.json()['oid']
        
        return await self.users_repository.get_user_adresses(user_id)
        