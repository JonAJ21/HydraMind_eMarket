from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from settings.config import settings

from asyncpg import Pool

@dataclass
class BaseCatalogRepository(ABC):
    
    @abstractmethod
    async def add_category(self) -> None:
        ...
        
@dataclass
class PostgreCatalogRepository(BaseCatalogRepository):
    _connection_pool: Pool = settings.postgre_sql_pool.pool
    
    async def add_category(self):
        return await super().add_category()
                
                    
                
                
        
        
        
        