from fastapi import APIRouter, Depends, HTTPException, status
import httpx

from application.api.v1.gateway.notification_schemas import AddNotificationRequestScheme
from settings.config import services
from application.api.v1.gateway.auth import oauth2_bearer, http_bearer

router = APIRouter(
    tags=['notification-service']
)

@router.post(
    '/add'
)
async def add_user_notification(
    scheme: AddNotificationRequestScheme
):
    '''Add notification'''
    
    async with httpx.AsyncClient() as client:
        url = f"{services['notification']}{'/add/notification'}"
        scheme_json = {
            'user_id': scheme.user_id,
            'text': scheme.text
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
async def get_limit_notifications(
    count_limit: int,
    token: str = Depends(oauth2_bearer)
):
    '''Get limit notifications'''
    async with httpx.AsyncClient() as client:
        url = f"{services['notification']}{'/get'}"
        schema = {
            'token' : token,
            'count_limit' : count_limit
        }
        response = await client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()

@router.get(
    '/get/unread'
)
async def get_unread_notifications(
    token: str = Depends(oauth2_bearer)
):
    '''Get unread notifications'''
    async with httpx.AsyncClient() as client:
        url = f"{services['notification']}{'/get/unread'}"
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