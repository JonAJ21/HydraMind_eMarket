from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from asyncpg import Pool

from domain.entities.product_storage_count import ProductStorage, ProductStorageCount
from domain.entities.product import Product
from domain.entities.storage import Storage
from settings.config import settings

@dataclass
class BaseStorageRepository(ABC):
    
    @abstractmethod
    async def get_storage_id(
        self, region: str, locality: str,
        street: str, building: str
    ) -> str | None:
        ...   
     
    @abstractmethod
    async def add_storage(self, storage: Storage) -> None:
        ...
      
    @abstractmethod
    async def get_product_count_from_storage(self, product_id: str, storage_id: str) -> int | None:
        ...  
    
    @abstractmethod
    async def insert_product_count_in_storage(self, product_id: str, storage_id: str, count: int) -> None:
        ...
   
    @abstractmethod
    async def set_product_count_to_storage(self, product_id: str, storage_id: str, count: int) -> None:
        ...
        
    @abstractmethod
    async def get_products_info_by_salesman(self, salesman_id: str) -> List[ProductStorage]:
        ...
        
@dataclass
class PostgreStorageRepository(BaseStorageRepository):
    _connection_pool: Pool = settings.postgre_sql_pool.pool
    
    async def get_storage_id(
        self, region: str, locality: str,
        street: str, building: str
    ) -> str | None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT storage_id
                    FROM storages
                    WHERE region = $1 AND locality = $2 AND street = $3 AND building = $4;
                '''
                
                row = await connection.fetchrow(
                    query,
                    region, locality, street, building
                )
                if row is not None:
                    return str(row['storage_id'])
        return None   
    
    
    async def add_storage(self, storage: Storage) -> None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    INSERT INTO storages
                        (storage_id, region, locality, street, building)
                    VALUES ($1, $2, $3, $4, $5);
                '''

                await connection.execute(
                    query, storage.oid, storage.region,
                    storage.locality, storage.street, storage.building
                )
                
    async def get_product_count_from_storage(self, product_id: str, storage_id: str) -> int | None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT count
                    FROM product_storage_count
                    WHERE product_id = $1 AND storage_id = $2;
                '''
                
                row = await connection.fetchrow(
                    query,
                    product_id, storage_id
                )
                
                if row is not None:
                    return int(row['count'])
        
        return None
    
    async def insert_product_count_in_storage(self, product_id: str, storage_id: str, count: int) -> None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    INSERT INTO product_storage_count
                        (product_id, storage_id, count)
                    VALUES ($1, $2, $3);
                '''

                await connection.execute(
                    query, product_id, storage_id, count
                )
        
    async def set_product_count_to_storage(self, product_id: str, storage_id: str, count: int) -> None:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    UPDATE product_storage_count
                        SET count = $3
                    WHERE product_id = $1 AND storage_id = $2;
                '''

                await connection.execute(
                    query, product_id, storage_id, count
                )
                
    async def get_products_info_by_salesman(self, salesman_id: str) -> List[ProductStorage]:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                
                query = '''
                    SELECT p.*, psc.count, s.*
                    FROM products p
                    LEFT JOIN product_storage_count psc ON p.product_id=psc.product_id
                    LEFT JOIN storages s ON psc.storage_id=s.storage_id
                    WHERE p.salesman_id = $1;
                '''
                
                rows = await connection.fetch(
                    query,
                    salesman_id
                )
                data = []
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
                    psc = ProductStorageCount(
                        product_id=str(row['product_id']),
                        storage_id=str(row['storage_id']),
                        count=row['count']
                    )
                    storage = Storage(
                        oid=str(row['storage_id']),
                        region=str(row['region']),
                        locality=str(row['locality']),
                        street=str(row['street']),
                        building=str(row['building'])
                    )
                    
                    
                    data.append(ProductStorage(product=product, storage=storage, psc=psc))
                return data
        
        