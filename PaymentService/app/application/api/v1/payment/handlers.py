
from fastapi import APIRouter, Depends, HTTPException, status

from logic.queries.payment import GetPaymentStatusQuery
from domain.exceptions.base import ApplicationException
from logic.mediator import Mediator
from logic.init import init_container
from application.api.v1.schemas import ErrorSchema
from application.api.v1.payment.schemas import GetPaymentStatusResponseSchema, GetPaymentStatusRequestSchema

router = APIRouter(
    tags=['payment']
)

@router.get(
    '/get/payment/status',
    response_model=GetPaymentStatusResponseSchema,
    status_code=status.HTTP_200_OK,
    description='Get payment status',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_payment_status_handler(
    scheme: GetPaymentStatusRequestSchema,
    container = Depends(init_container)
):
    '''Get payment status'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        payment_status, *_ = await mediator.handle_query(
            GetPaymentStatusQuery(
                name = scheme.name,
                price = scheme.price
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    return GetPaymentStatusResponseSchema.from_entity(payment_status=payment_status)