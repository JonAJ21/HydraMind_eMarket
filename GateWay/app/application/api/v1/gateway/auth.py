from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
import httpx

from application.api.v1.gateway.auth_schemas import RegisterUserRequestSchema
from settings.config import services

http_bearer = HTTPBearer()

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl='/auth/login'
)

router = APIRouter(
    tags=['auth-service']
)

@router.post(
    '/register'
)
async def register_user_handler(
    schema: RegisterUserRequestSchema
):
    '''Register new user'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['auth']}{'/register'}"
        response = await client.request('POST', url, json=schema.json(), headers=None)
    
    
    if response.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=response.json()
        )    
        
    return response.json()
        

@router.post(
    '/login'
)
async def login_user_handler(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    '''Login user'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['auth']}{'/login'}"
        schema = {
            'login': username,
            'password': password
        }
        response = await client.request('POST', url, json=schema, headers=None)
    
    if response.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    
    return response.json()


@router.post(
    '/refresh'
)
async def auth_refresh_jwt_handler(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]
):  
    '''Refresh user'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['auth']}{'/refresh'}"
        schema = {
            'token' : credentials.credentials
        }
        response = await client.request('POST', url, json=schema, headers=None)
    
    if response.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.get(
    '/user'
)
async def get_auth_user_info(
    token: str = Depends(oauth2_bearer)
):
    '''Auth user'''
    async with httpx.AsyncClient() as client:
        url = f"{services['auth']}{'/user/info'}"
        schema = {
            'token' : token
        }
        response = await client.request('GET', url, json=schema, headers=None)
        
    if response.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    return response.json()
    
    


    
    
            