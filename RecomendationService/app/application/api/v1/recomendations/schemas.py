from typing import List

from pydantic import BaseModel

from domain.entities.recomendation import Recomendation


class GetRecomendationRequestScheme(BaseModel):
    token: str
    n_recommendations: int


class GetRecomendationResponseScheme(BaseModel):
    recomendation: str | None = None

class GetRecomendationsResponseScheme(BaseModel):
    user_id: str
    recomendations: List[GetRecomendationResponseScheme]
    

    @classmethod
    def from_entity(cls, recomendation: Recomendation) -> 'GetRecomendationsResponseScheme':
        recomendations = []
        for product in recomendation.recommended_products:
            # print("recomendation ", recomendation)
            if product == []:
                recomendation_scheme = GetRecomendationResponseScheme(recomendation=None)
            else:
                recomendation_scheme = GetRecomendationResponseScheme(recomendation=product)
            recomendations.append(recomendation_scheme)
        
        print("recomendations", recomendations)
        return GetRecomendationsResponseScheme(
            user_id=recomendation.user_id,
            recomendations=recomendations
        )
        
class GenerateRecomendationsRequestScheme(BaseModel):
    token: str
    n_recommendations: int

class GenerateRecomendationsResponseScheme(BaseModel):
    message: str
