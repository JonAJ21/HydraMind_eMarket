from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import httpx

from infrastructure.models.recomendation import BaseRecomendationModel
from logic.exceptions.user import BadRequestToAuthServiceException
from infrastructure.repositories.recomendation import BaseRecomendationRepository
from domain.entities.recomendation import Recomendation
from settings.config import settings


@dataclass
class BaseRecomendationService(ABC):
    
    @abstractmethod
    async def generate_recomendation(self, token: str, n_recommendations: int) -> Recomendation:
        ...
        
    @abstractmethod
    async def get_recomendation(self, token: str, n_recommendations: int) -> Recomendation:
        ...
    
    
    
@dataclass
class RESTRecomendationService(BaseRecomendationService):
    recomendation_repository: BaseRecomendationRepository
    recomendation_model: BaseRecomendationModel
    
    
    async def generate_recomendation(self, token: str, n_recommendations: int) -> Recomendation:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        user_id = response.json()['oid']
        
        recomendation = Recomendation(
            user_id=user_id,
            recommended_products= await self.recomendation_model.generate_recommendation(user_id)
        )
        
        await self.recomendation_repository.add_recomendations(recomendation)
        
        return recomendation

        
        
    async def get_recomendation(self, token: str, n_recommendations: int) -> Recomendation:
        async with httpx.AsyncClient() as client:
            url = f"{settings.services.auth}{'/user/info'}"
            schema = {
                'token' : token
            }
            response = await client.request('GET', url, json=schema, headers=None)
        
        if response.is_error:
            raise BadRequestToAuthServiceException()
        
        user_id = response.json()['oid']
        
        return await self.recomendation_repository.get_recomendations(user_id, n_recommendations)
