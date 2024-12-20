from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from settings.config import services
from application.api.v1.gateway.auth import oauth2_bearer, http_bearer

router = APIRouter(
    tags=['order-service']
)

@router.post(
    '/create/order'
)
async def create_order(
    token: str = Depends(oauth2_bearer)
):
    '''Create order'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/create/order'}"
        print(url)
        scheme_json = {
            'token' : token,
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
async def add_order_product(
    product_id: str,
    count: int,
    token: str = Depends(oauth2_bearer)
):
    '''Create order'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/add/order/product'}"
        print(url)
        scheme_json = {
            'token' : token,
            'product_id': product_id,
            'count': count
        }
        response = await client.request('POST', url, json=scheme_json, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.get(
    '/get/order/info'
)
async def add_order_product(
    order_id: str,
    token: str = Depends(oauth2_bearer)
):
    '''Get order info'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/get/order/info'}"
        print(url)
        scheme_json = {
            'token' : token,
            'order_id': order_id
        }
        response = await client.request('GET', url, json=scheme_json, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.get(
    '/get/orders/info'
)
async def add_order_product(
    limit: int,
    token: str = Depends(oauth2_bearer)
):
    '''Get order info'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/get/orders/info'}"
        print(url)
        scheme_json = {
            'token' : token,
            'limit': limit
        }
        response = await client.request('GET', url, json=scheme_json, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.post(
    '/change/order/status'
)
async def add_order_product(
    order_id: str,
    order_status: str,
    token: str = Depends(oauth2_bearer)
):
    '''Create order'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['catalog']}{'/change/order/status'}"
        print(url)
        scheme_json = {
            'token' : token,
            'order_id': order_id,
            'status': order_status
        }
        response = await client.request('POST', url, json=scheme_json, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()