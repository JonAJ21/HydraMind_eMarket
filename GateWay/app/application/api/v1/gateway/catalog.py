from fastapi import APIRouter, Depends, HTTPException, status
import httpx

from application.api.v1.gateway.catalog_scheme import AddCategoryRequestScheme, AddProductRequestScheme, AddStorageRequestScheme
from settings.config import services
from application.api.v1.gateway.auth import oauth2_bearer, http_bearer

router = APIRouter(
    tags=['catalog-service']
)

@router.post(
    '/add/category'
)
async def add_category(
    scheme: AddCategoryRequestScheme,
    token: str = Depends(oauth2_bearer)
):
    '''Add category'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/add/category'}"
        scheme_json = {
            'token' : token,
            'parent_category': scheme.parent_category,
            'category_name': scheme.category_name
        }
        response = await client.request('POST', url, json=scheme_json, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.post(
    '/add/product'
)
async def add_product(
    scheme: AddProductRequestScheme,
    token: str = Depends(oauth2_bearer)
):
    '''Add product'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/add/product'}"
        scheme_json = {
            'token' : token,
            'name': scheme.name,
            'category_name': scheme.category_name,
            'description': scheme.description,
            'price': scheme.price,
            'discount_percent': scheme.discount_percent
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
async def get_products_by_category(
    category_name: str,
):
    '''Get products by category'''
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/get/category/products'}"
        schema = {
            'category_name' : category_name,
        }
        response = await client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()


@router.get(
    '/get/categories'
)
async def get_categories(
):
    '''Get categories'''
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/get/categories'}"
        schema = {
        }
        response = await client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.post(
    '/add/storage'
)
async def add_storage(
    scheme: AddStorageRequestScheme,
    token: str = Depends(oauth2_bearer)
):
    '''Add product'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/add/storage'}"
        scheme_json = {
            'token' : token,
            'region' : scheme.region,
            'locality' : scheme.locality,
            'street' : scheme.street,
            'building' : scheme.building
            
        }
        response = await client.request('POST', url, json=scheme_json, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()