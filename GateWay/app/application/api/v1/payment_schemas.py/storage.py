from fastapi import APIRouter, Depends, HTTPException, status
import httpx

from application.api.v1.gateway.storage_schemas import AddProductToStorageRequestScheme, TakeProductFromStorageRequestScheme
from application.api.v1.gateway.catalog_scheme import AddStorageRequestScheme
from settings.config import services
from application.api.v1.gateway.auth import oauth2_bearer, http_bearer

router = APIRouter(
    tags=['storage-service']
)

@router.post(
    '/add/storage'
)
async def add_storage(
    scheme: AddStorageRequestScheme,
    token: str = Depends(oauth2_bearer)
):
    '''Add storage'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/add/storage'}"
        print(url)
        scheme_json = {
            'token' : token,
            'region': scheme.region,
            'locality': scheme.locality,
            'street': scheme.street,
            'building': scheme.building
        }
        response = await client.request('POST', url, json=scheme_json, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.post(
    '/add/storage/product'
)
async def add_product_to_storage(
    scheme: AddProductToStorageRequestScheme,
    token: str = Depends(oauth2_bearer)
):
    '''Add product to storage'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/add/storage/product'}"
        
        scheme_json = {
            'token' : token,
            'product_id': scheme.product_id,
            'storage_id': scheme.storage_id,
            'count': scheme.count
        }
        response = await client.request('POST', url, json=scheme_json, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.post(
    '/take/storage/product'
)
async def take_products_from_storage(
    scheme: TakeProductFromStorageRequestScheme,
    token: str = Depends(oauth2_bearer)
):
    '''Take product from storage'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/take/storage/product'}"
        
        scheme_json = {
            'token' : token,
            'product_id': scheme.product_id,
            'storage_id': scheme.storage_id,
            'count': scheme.count
        }
        response = await client.request('POST', url, json=scheme_json, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.get(
    '/get/products'
)
async def get_products_by_salesman(
    token: str = Depends(oauth2_bearer)
):
    '''Get products by salesman'''
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/get/salesman/products'}"
        schema = {
            'token' : token,
        }
        response = await client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()
