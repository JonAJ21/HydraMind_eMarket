from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from settings.config import services
from application.api.v1.gateway.auth import oauth2_bearer


router = APIRouter(
    tags=['recomendations-service']
)

@router.post(
    '/generate'
)
async def generate_recomendations(
    n_recommendations: int,
    token: str = Depends(oauth2_bearer)
):
    '''Generate recomendations'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['recomendations']}{'/generate/recomendations'}"
        print(url)
        scheme_json = {
            'token' : token,
            'n_recommendations': n_recommendations
        }
        response = await client.request('POST', url, json=scheme_json, headers=None)

    
    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.get(
    '/get'
)
async def get_recomendations(
    n_recommendations: int,
    token: str = Depends(oauth2_bearer)
):
    '''Get recomendations'''
    async with httpx.AsyncClient() as client:
        url = f"{services['recomendations']}{'/get/recomendations'}"
        print(url)
        scheme_json = {
            'token' : token,
            'n_recommendations': n_recommendations
        }
        response = await client.request('GET', url, json=scheme_json, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()