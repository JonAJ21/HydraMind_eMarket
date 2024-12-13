from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import httpx

from domain.entities.product import Product
from logic.exceptions.catalog import CategoryDoesNotExistException, CategoryWithNameAlreadyExistsException
from logic.exceptions.user import BadRequestToAuthServiceException, PermissionDeniedException
from infrastructure.repositories.catalog import BaseCatalogRepository
from domain.entities.category import Category
from settings.config import settings


@dataclass
class BaseCatalogService(ABC):
    
    @abstractmethod
    async def add_category(
        self, token: str, parent_category: str, category_name: str
    ) -> Category:
        ...
        
    @abstractmethod
    async def add_product(
        self, token: str, name: str, category_name: str,
        description: str, price: float, discount_percent: float
    ) -> Product:
        ...
        
    @abstractmethod
    async def get_products_by_category(
        self, category_name: str
    ) -> List[Product]:
        ...
    
    
    
@dataclass
class RESTCatalogService(BaseCatalogService):
    catalog_repository: BaseCatalogRepository
    
    async def add_category(self, token: str, parent_category: str, category_name: str) -> Category:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        if response.json()['role'] not in ['ADMIN', 'SALESMAN']:
            raise PermissionDeniedException(valid_roles=['ADMIN', 'SALESMAN'], role=response.json()['role'])
        
        category_name_exists = await self.catalog_repository.get_category_id(category_name)
        if category_name_exists is not None:
            raise CategoryWithNameAlreadyExistsException(category_name)
        
        parent_category_id = '3f591be6-a395-4011-9e5c-a6ce77ce3d15' # uuid for root
        if parent_category != '':
            parent_category_id = await self.catalog_repository.get_category_id(parent_category)
        
        if parent_category_id is None:
            raise CategoryDoesNotExistException(parent_category)
        
        category = Category(
            parent_category=parent_category,
            category_name=category_name
        )
        
        await self.catalog_repository.add_category(category.oid, category_name, parent_category_id)
        
        return category

    async def add_product(
        self, token, name, category_name,
        description, price, discount_percent
    ) -> Product:
        
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
        
        category_id = await self.catalog_repository.get_category_id(category_name)
        if category_id is None:
            raise CategoryDoesNotExistException(category_name)
        
        product = Product(
            name=name,
            salesman_id=response.json()['oid'],
            category_id=category_id,
            description=description,
            rating=None,
            price=price,
            discount_percent=discount_percent
        )
        
        await self.catalog_repository.add_product(product)
        
        return product
    
    async def get_products_by_category(self, category_name: str) -> List[Product]:
        category_id = await self.catalog_repository.get_category_id(category_name)
        if category_id is None:
            raise CategoryDoesNotExistException(category_name)
        
        return await self.catalog_repository.get_products_by_category(category_id)
        
    
