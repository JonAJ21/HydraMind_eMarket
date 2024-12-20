from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from asyncpg import Pool

from domain.entities.product import Product
from domain.entities.order import Order
from settings.config import settings

@dataclass
class BaseOrderRepository(ABC):
    
    @abstractmethod
    async def create_order(self, order: Order) -> None:
        ...
        
    @abstractmethod
    async def add_product_to_order(self, order_id: str, product_id: str, count: int) -> None:
        ...
    
    @abstractmethod
    async def get_last_created_order_id(self, user_id) -> str | None:
        ...
    
    @abstractmethod
    async def get_order_info(self, order_id: str) -> Order:
        ...
    
    @abstractmethod
    async def get_user_order_ids(self, user_id: str, limit: int) -> List[str]:
        ...
        
    @abstractmethod
    async def change_order_status(self, order_id: str, status: str) -> None:
        ...
        
@dataclass
class PostgreOrderRepository(BaseOrderRepository):
    _connection_pool: Pool = settings.postgre_sql_pool.pool
    
    async def create_order(self, order):
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    INSERT INTO orders
                        (order_id, user_id, time_created, time_delivered, status, is_paid)
                    VALUES ($1, $2, $3, $4, $5, $6);
                '''

                await connection.execute(
                    query, order.oid, order.user_id,
                    order.time_created, order.time_delivered,
                    order.status, order.is_paid
                )
                
    async def add_product_to_order(self, order_id: str, product_id: str, count: int) -> None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    INSERT INTO order_product_count
                        (order_id, product_id, count)
                    VALUES ($1, $2, $3);
                '''

                await connection.execute(
                    query, order_id, product_id, count
                )
    
    async def get_last_created_order_id(self, user_id) -> str | None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT order_id
                    FROM orders
                    WHERE user_id = $1 AND status = 'CREATED'
                    ORDER BY time_created DESC
                    LIMIT 1
                '''
                row = await connection.fetchrow(
                    query, user_id
                )
                
                if row is None:
                    return None
                
                return row['order_id']
                
        
    async def get_order_info(self, order_id: str) -> Order:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT o.*, opc.count, p.*
                    FROM orders o
                    LEFT JOIN order_product_count opc ON o.order_id=opc.order_id
                    LEFT JOIN products p ON opc.product_id=p.product_id
                    WHERE o.order_id = $1;
                '''
                
                rows = await connection.fetch(
                    query,
                    order_id
                )

                products = []
                for row in rows:
                    order = Order(
                        oid=order_id,
                        user_id = row['user_id'],
                        time_created=row['time_created'],
                        time_delivered=row['time_delivered'],
                        status=row['status'],
                        is_paid=row['is_paid']
                    )
                    product = Product(
                        oid = str(row['product_id']),
                        name = str(row['name']),
                        salesman_id = str(row['salesman_id']),
                        category_id = str(row['category_id']),
                        description = str(row['description']),
                        rating = row['rating'],
                        price = float(row['price']),
                        discount_percent = float(row['discount_percent']),
                        count= row['count']
                    )
                    products.append(product)
                
                order.products = products
                
                return order
        
    async def get_user_order_ids(self, user_id: str, limit: int) -> List[str]:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT order_id
                    FROM orders
                    WHERE user_id = $1
                    ORDER BY time_created
                    LIMIT $2
                '''
                rows = await connection.fetch(
                    query, user_id, limit
                )
                
                ids = []
                for row in rows:
                    ids.append(row['order_id'])
                
                return ids
                
    async def change_order_status(self, order_id: str, status: str) -> None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    UPDATE orders
                        SET status = $2
                    WHERE order_id = $1;      
                '''
                
                await connection.execute(query, order_id, status)
                