from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

import pandas as pd
from sklearn.neighbors import NearestNeighbors

from infrastructure.repositories.recomendation import BaseRecomendationRepository
from domain.entities.recomendation import Recomendation
from settings.config import settings

from asyncpg import Pool

@dataclass
class BaseRecomendationModel(ABC):
    
    @abstractmethod
    async def fit(self) -> None:
        ...
    
    @abstractmethod
    async def generate_recommendation(self, user_id: str, n_recommendations: int = 5) -> List[str]:
        ...
        
    
@dataclass
class KNNRecomendationModel(BaseRecomendationModel):
    recomendation_repository: BaseRecomendationRepository
    model: NearestNeighbors | None = None
    user_product_matrix: pd.DataFrame = field(default_factory=pd.DataFrame)
    n_neighbors: int = 6
    
    async def _create_user_product_matrix(self, orders_df: pd.DataFrame) -> pd.DataFrame:
        user_product_matrix = orders_df.pivot_table(
            index='user_id',
            columns='product_id',
            values='count',
            aggfunc='sum',
            fill_value=0
        )
        return user_product_matrix
    
    async def _fit_model(self, user_product_matrix: pd.DataFrame) -> None:
        n_users = user_product_matrix.shape[0]
        self.n_neighbors = min(self.n_neighbors, n_users)
        self.model = NearestNeighbors(
            metric='cosine',
            algorithm='brute',
            n_neighbors=self.n_neighbors,
            n_jobs=-1
        )
        self.model.fit(user_product_matrix.values)
    
    async def fit(self) -> None:
        orders_df, products_df, users_df = await self.recomendation_repository.load_data()
        self.user_product_matrix = await self._create_user_product_matrix(orders_df)
        await self._fit_model(self.user_product_matrix)
        
    
    async def generate_recommendation(self, user_id: str, n_recommendations: int = 5) -> List[str]:
        """
        Генерирует рекомендации для заданного пользователя.
        """
        if user_id not in self.user_product_matrix.index:
            print(f"Пользователь с ID {user_id} не найден.")
            return []

        # Вектор пользователя
        user_vector = self.user_product_matrix.loc[user_id].values.reshape(1, -1)

        # Поиск ближайших соседей
        distances, indices = self.model.kneighbors(user_vector, n_neighbors=self.n_neighbors)

        # Получение ID соседей (исключая самого пользователя)
        similar_users = []
        for idx in indices.flatten():
            similar_user_id = self.user_product_matrix.index[idx]
            if similar_user_id != user_id:
                similar_users.append(similar_user_id)

        if not similar_users:
            return []

        # Суммирование покупок соседей
        similar_users_purchases = self.user_product_matrix.loc[similar_users].sum(axis=0)

        # Исключение товаров, уже купленных пользователем
        purchased = self.user_product_matrix.loc[user_id]
        recommendations = similar_users_purchases[purchased == 0].sort_values(ascending=False)

        # Возвращение топ-N рекомендаций
        top_recommendations = recommendations.head(n_recommendations).index.tolist()
        
        return top_recommendations.tolist()
    
