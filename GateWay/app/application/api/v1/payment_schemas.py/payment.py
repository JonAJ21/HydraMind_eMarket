
from fastapi import APIRouter, Depends, HTTPException, status
import httpx

from settings.config import services
from application.api.v1.gateway.payment_schemas import GetPaymentStatusResponseSchema, GetPaymentStatusRequestSchema


router = APIRouter(
    tags=['payment-service']
)

@router.get(
    '/get/payment/status'
)
async def get_payment_status_handler(
    scheme: GetPaymentStatusRequestSchema
):
    '''Get payment status'''
    async with httpx.AsyncClient() as client:
        url = f"{services['payment']}{'/get/payment/status'}"
        scheme_json = {
            'name': scheme.name,
            'price': scheme.price
        }
        response = await client.request('GET', url, json=scheme_json, headers=None)

    if response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.json()
        )
    
    return response.json()