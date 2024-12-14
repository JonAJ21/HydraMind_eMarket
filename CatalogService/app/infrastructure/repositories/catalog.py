from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from domain.entities.category import Category
from domain.entities.product import Product
from settings.config import settings

from asyncpg import Pool

@dataclass
class BaseCatalogRepository(ABC):
    
    @abstractmethod
    async def get_category_id(self, category_name: str) -> str | None:
        ...
    
    @abstractmethod
    async def add_category(self, category_id: str, category_name: str, parent_category_id: str) -> None:
        ...
        
    @abstractmethod
    async def get_categories(self) -> List[Category]:
        ...
        
    @abstractmethod
    async def add_product(self, product: Product) -> None:
        ...
        
    @abstractmethod
    async def get_products_by_category(self, category_id: str) -> List[Product]:
        ...
        
@dataclass
class PostgreCatalogRepository(BaseCatalogRepository):
    _connection_pool: Pool = settings.postgre_sql_pool.pool
    
    async def get_category_id(self, category_name: str) -> str | None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT category_id 
                    FROM categories
                    WHERE name = $1;
                '''
                
                row = await connection.fetchrow(
                    query,
                    category_name
                )
                if row is not None:
                    return str(row['category_id'])
        return None
    
    async def add_category(self, category_id: str, category_name: str, parent_category_id: str) -> None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    INSERT INTO categories
                        (category_id, name, parent_category_id)
                    VALUES ($1, $2, $3);
                '''

                await connection.execute(
                    query, category_id,
                    category_name, parent_category_id
                )
                       
    async def get_categories(self) -> List[Category]:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT category_id, name, parent_category_id
                    FROM categories
                '''
                
                rows = await connection.fetch(
                    query
                )
                
                categories = []
                for row in rows:
                    category = Category(
                        oid=str(row['category_id']),
                        category_name=str(row['name']),
                        parent_category=str(row['parent_category_id'])
                    )
                    categories.append(category)
                return categories
                    
              
    async def add_product(self, product: Product) -> None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    INSERT INTO products
                        (product_id, name, salesman_id, category_id, description, price, discount_percent)
                    VALUES ($1, $2, $3, $4, $5, $6, $7);
                '''

                await connection.execute(
                    query, product.oid, 
                    product.name, product.salesman_id,
                    product.category_id, product.description, 
                    product.price, product.discount_percent
                )
    
    async def get_products_by_category(self, category_id: str) -> List[Product]:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT product_id, name, salesman_id, category_id, description, rating, price, discount_percent
                    FROM products
                    WHERE category_id = $1;
                '''
                rows = await connection.fetch(
                    query, category_id
                )
                
                products = []
                for row in rows:
                    
                    product = Product(
                        oid = str(row['product_id']),
                        name = str(row['name']),
                        salesman_id = str(row['salesman_id']),
                        category_id = str(row['category_id']),
                        description = str(row['description']),
                        rating = row['rating'],
                        price = float(row['price']),
                        discount_percent = float(row['discount_percent'])
                    )
                    products.append(product)
        
        return products
    
        
        
        