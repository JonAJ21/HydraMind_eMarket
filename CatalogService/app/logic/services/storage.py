from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import httpx

from domain.entities.product_storage_count import ProductStorage
from logic.exceptions.storage import NoProductInStorageException, NotEnoughProductInStorageException, StorageAlreadyExistsException
from logic.exceptions.user import BadRequestToAuthServiceException, PermissionDeniedException
from infrastructure.repositories.storage import BaseStorageRepository
from domain.entities.storage import Storage
from settings.config import settings

@dataclass
class BaseStorageService(ABC):
    
    @abstractmethod
    async def add_storage(
        self, token: str, region: str, locality: str, street: str, building: str
    ) -> Storage:
        ...
        
    @abstractmethod
    async def add_product_to_storage(
        self, token: str, product_id: str, storage_id: str, count: int
    ) -> int:
        ...
        
    @abstractmethod
    async def take_product_count_from_storage(
        self, token: str, product_id: str, storage_id: str, count: int
    ) -> int:
        ...
        
    @abstractmethod
    async def get_products_info_by_salesman(
        self, token: str
    ) -> List[ProductStorage]:
        ...
        
@dataclass
class RESTStorageService(BaseStorageService):
    storage_repository: BaseStorageRepository
    
    async def add_storage(
        self, token: str, region: str,
        locality: str, street: str, building: str 
    ) -> Storage:
        
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        if response.json()['role'] not in ['ADMIN']:
            raise PermissionDeniedException(valid_roles=['ADMIN'], role=response.json()['role'])
        
        storage_id = await self.storage_repository.get_storage_id(region, locality, street, building)
        if storage_id is not None:
            raise StorageAlreadyExistsException()
        
        storage = Storage(
            region=region,
            locality=locality,
            street=street,
            building=building
        )
        
        await self.storage_repository.add_storage(storage)
        
        return storage
    
    async def add_product_to_storage(
        self, token: str, product_id: str, storage_id: str, count: int
    ) -> int:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        if response.json()['role'] not in ['SALESMAN']:
            raise PermissionDeniedException(valid_roles=['SALESMAN'], role=response.json()['role'])
        
        count_in_storage = await self.storage_repository.get_product_count_from_storage(product_id, storage_id)
        if count_in_storage is None:
            await self.storage_repository.insert_product_count_in_storage(product_id, storage_id, count)            
            return count
        
        count_in_storage += count
        await self.storage_repository.set_product_count_to_storage(
            product_id, storage_id, count_in_storage
        )
        
        return count_in_storage
    
    async def take_product_count_from_storage(
        self, token: str, product_id: str, storage_id: str, count: int
    ) -> int:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)

        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        if response.json()['role'] not in ['SALESMAN']:
            raise PermissionDeniedException(valid_roles=['SALESMAN'], role=response.json()['role'])
        
        count_in_storage = await self.storage_repository.get_product_count_from_storage(product_id, storage_id)
        if count_in_storage is None:
            raise NoProductInStorageException()
        
        if count_in_storage - count < 0:
            raise NotEnoughProductInStorageException(count_in_storage=count_in_storage)
        
        count_in_storage -= count
        await self.storage_repository.set_product_count_to_storage(product_id, storage_id, count_in_storage)
        return count_in_storage
        
    async def get_products_info_by_salesman(self, token: str) -> List[ProductStorage]:    
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)

        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        if response.json()['role'] not in ['SALESMAN']:
            raise PermissionDeniedException(valid_roles=['SALESMAN'], role=response.json()['role'])
        
        return await self.storage_repository.get_products_info_by_salesman(response.json()['oid'])
    
         
        