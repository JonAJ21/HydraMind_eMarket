from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd

from domain.entities.recomendation import Recomendation
from settings.config import settings

from asyncpg import Pool, UniqueViolationError

@dataclass
class BaseRecomendationRepository(ABC):
    
    @abstractmethod
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        ...
    
    @abstractmethod
    async def add_recomendations(self, recomendations: Recomendation) -> None:
        ...
    
    @abstractmethod
    async def get_recomendations(self, user_id: str, n_recommendations: int = 5) -> Recomendation:
        ...
    
        
@dataclass
class PostgreRecomendationRepository(BaseRecomendationRepository):
    _connection_pool: Pool = settings.postgre_sql_pool.pool
    
    async def read_sql_to_df(self, query: str, connection: Pool) -> pd.DataFrame:
        # Выполняем запрос и получаем записи
        records = await connection.fetch(query)
        
        if not records:
            return pd.DataFrame()
        
        # Получаем названия колонок из первой записи
        columns = [key for key in records[0].keys()]
        
        # Преобразуем записи в список словарей
        data = [dict(record) for record in records]
        
        # Создаем DataFrame
        return pd.DataFrame(data, columns=columns)
    
    async def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                orders_query = '''
                    SELECT o.user_id, opc.product_id, opc.count
                    FROM orders o
                    JOIN order_product_count opc ON o.order_id = opc.order_id
                    WHERE o.status = 'delivered' AND o.is_paid = TRUE;
                '''
                orders_df = await self.read_sql_to_df(orders_query, connection)
                
                products_query = "SELECT product_id, name, category_id FROM products;"
                products_df = await self.read_sql_to_df(products_query, connection)

                users_query = "SELECT user_id, login FROM users;"
                users_df = await self.read_sql_to_df(users_query, connection)
                
                return (orders_df, products_df, users_df)
    
    async def add_recomendations(self, recomendation: Recomendation) -> None:
        try:
            async with self._connection_pool.acquire() as connection:
                async with connection.transaction():
                        query = '''
                            INSERT INTO user_recommendations (user_id, recommended_products, generated_at)
                            VALUES ($1, $2, $3);
                        '''
                        await connection.execute(
                            query, recomendation.user_id,
                            recomendation.recommended_products,
                            recomendation.generated_at)
        except UniqueViolationError as e:
            async with self._connection_pool.acquire() as connection:
                async with connection.transaction():
                    query = '''
                        UPDATE user_recommendations
                        SET recommended_products = $2, generated_at = $3
                        WHERE user_id = $1;
                    '''
                    await connection.execute(
                        query, recomendation.user_id,
                        recomendation.recommended_products,
                        recomendation.generated_at)
                
                
    
    async def get_recomendations(self, user_id: str, n_recommendations: int = 5) -> Recomendation:
        async with self._connection_pool.acquire() as connection:
            async with connection.transaction():
                query = '''
                    SELECT user_id, recommended_products, generated_at
                    FROM user_recommendations
                    WHERE user_id = $1
                    ORDER BY generated_at DESC
                    LIMIT $2;
                '''
                
                rows = await connection.fetch(query, user_id, n_recommendations)
                
                recomendation = Recomendation(
                    user_id=str(rows[0]['user_id']),
                    recommended_products=[],
                    generated_at=rows[0]['generated_at']
                )
                for row in rows:
                    recomendation.recommended_products.append(row['recommended_products'])
                    
                return recomendation