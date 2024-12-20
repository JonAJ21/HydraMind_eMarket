from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import httpx

from logic.exceptions.order import OrderWasNotCreatedException
from logic.exceptions.user import BadRequestToAuthServiceException
from infrastructure.repositories.order import BaseOrderRepository
from domain.entities.order import Order
from settings.config import settings

@dataclass
class BaseOrderService(ABC):
    
    @abstractmethod
    async def create_order(
        self, token: str
    ) -> Order:
        ...
        
    @abstractmethod
    async def add_product_to_order(self, token: str, product_id, count: int) -> None:
        ...
        
    @abstractmethod
    async def get_order_info(self, token: str, order_id: str) -> Order:
        ...
    
    @abstractmethod
    async def get_orders_info(self, token: str, limit: int) -> List[Order]:
        ...
        
    @abstractmethod
    async def change_order_status(self, token: str, order_id: str, status: str) -> None:
        ...
    
    
@dataclass    
class RESTOrderService(BaseOrderService):
    order_repository: BaseOrderRepository
    
    async def create_order(self, token) -> Order:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        order = Order(
            user_id=response.json()['oid'],
            status='CREATED'
        )
        print('KDLS')
        await self.order_repository.create_order(order)
        
        return order
    
    async def add_product_to_order(self, token: str, product_id: str, count: int) -> None:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        user_id = response.json()['oid']
        
        order_id = await self.order_repository.get_last_created_order_id(user_id)
        
        if order_id is None:
            raise OrderWasNotCreatedException()
        
        await self.order_repository.add_product_to_order(order_id, product_id, count)
        
    async def get_order_info(self, token: str, order_id: str) -> Order:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        return await self.order_repository.get_order_info(order_id)
        
        
    async def get_orders_info(self, token: str, limit: int) -> List[Order]:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        user_id = response.json()['oid']
        
        orders = []
        
        ids = await self.order_repository.get_user_order_ids(user_id, limit)
        for id in ids:
            order = await self.get_order_info(token, id)
            orders.append(order)
            
        return orders
    
    async def change_order_status(self, token: str, order_id: str, status: str) -> None:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        await self.order_repository.change_order_status(order_id, status)