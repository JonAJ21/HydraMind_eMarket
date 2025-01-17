
from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
import httpx
from application.api.v1.gateway.user_schemas import AddUserAdressRequestScheme
from settings.config import services

from application.api.v1.gateway.auth import oauth2_bearer, http_bearer


router = APIRouter(
    tags=['user-service']
    
)


@router.get(
    '/info'
)
async def get_auth_user_info(
    token: str = Depends(oauth2_bearer)
):
    '''User Info'''
    async with httpx.AsyncClient() as client:
        url = f"{services['user']}{'/info'}"
        schema = {
            'token' : token
        }
        response = await client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()


@router.post(
    '/add/adress'
)
async def add_user_adress(
    scheme: AddUserAdressRequestScheme,
    token: str = Depends(oauth2_bearer)
):
    '''Add user adress'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['user']}{'/add/adress'}"
        schema = {
            'token' : token,
            'region' : scheme.region,
            'locality': scheme.locality,
            'street' : scheme.street,
            'building' : scheme.building
        }
        response = await client.request('POST', url, json=schema, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.get(
    '/get/adresses'
)
async def get_user_adresses(
    token: str = Depends(oauth2_bearer)
):
    '''Get adresses'''
    async with httpx.AsyncClient() as client:
        url = f"{services['user']}{'/get/adresses'}"
        schema = {
            'token' : token
        }
        response = await client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.put(
    '/delete/adress'
)
async def delete_user_adress(
    adress_id: str,
    token: str = Depends(oauth2_bearer)
):
    '''delete user adress'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['user']}{'/delete/adress'}"
        schema = {
            'token' : token,
            'adress_id': adress_id
        }
        response = await client.request('PUT', url, json=schema, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

# @router.put(
#     '/deactivate'
# )
# async def deactivate_user(
#     login: str,
#     token: str = Depends(oauth2_bearer)
# ):
#     '''Deactivate user'''
    
#     async with httpx.AsyncClient() as client:
#         url = f"{services['user']}{'/deactivate'}"
#         schema = {
#             'token' : token,
#             'login': login
#         }
#         response = await client.request('PUT', url, json=schema, headers=None)

#     if response.is_error:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=response.json()
#         )
    
#     return response.json()

# @router.put(
#     '/activate'
# )
# async def activate_user(
#     login: str,
#     token: str = Depends(oauth2_bearer)
# ):
#     '''Activate user'''
    
#     async with httpx.AsyncClient() as client:
#         url = f"{services['user']}{'/activate'}"
#         schema = {
#             'token' : token,
#             'login': login
#         }
#         response = await client.request('PUT', url, json=schema, headers=None)

#     if response.is_error:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=response.json()
#         )
    
#     return response.json()

@router.put(
    '/change/email'
)
async def change_user_email(
    new_email: Annotated[str, Form()],
    token: str = Depends(oauth2_bearer)
):
    '''Change Email'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['user']}{'/change/email'}"
        schema = {
            'token' : token,
            'new_email' : new_email
        }
        response = await client.request('PUT', url, json=schema, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.put(
    '/change/role'
)
async def change_user_role(
    login: str,
    new_role: str,
    token: str = Depends(oauth2_bearer)
):
    '''Change user role'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['user']}{'/change/role'}"
        schema = {
            'token' : token,
            'login': login,
            'new_role': new_role
        }
        response = await client.request('PUT', url, json=schema, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()














# @router.get(
#     '/hello'
# )
# async def get_test():
    
#     async with httpx.AsyncClient() as client:
#         url = f"{services['user']}{'/hello'}"
#         response = await client.request('GET', url, json=None, headers=None)
#     return response.json()





# async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
#     async with httpx.AsyncClient() as client:
#         url = f"{service_url}{path}"
#         response = await client.request(method, url, json=body, headers=headers)
#         return response
    
# @router.api_route(
#     "/{service}/{path:path}",
#     methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
# )
# async def gateway(service: str, path: str, request: Request):
#     if service not in services:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Service not found')
    
#     service_url = services[service]
#     body = await request.json() if request.method in  ['POST', 'PUT', 'PATCH'] else None
#     headers = dict(request.headers)
    
#     response = await forward_request(service_url, request.method, f"{path}", body, headers)
    
#     return JSONResponse(status_code=response.status_code, content=response.json())