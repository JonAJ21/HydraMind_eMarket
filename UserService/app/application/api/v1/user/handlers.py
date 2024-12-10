
from fastapi import APIRouter, Depends, HTTPException, status

from logic.commands.adress import AddAdressCommand
from logic.commands.email import ChangeEmailCommand
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from logic.init import init_container
from logic.mediator import Mediator
from logic.queries.get_user import GetUserInfoQuery
from application.api.v1.schemas import ErrorSchema
from application.api.v1.user.schemas import AddAdressRequestSchema, AddAdressResponseSchema, ChangeEmailRequestSchema, ChangeEmailResponseSchema, GetUserInfoRequestSchema, GetUserInfoResponseSchema


router = APIRouter(
    tags=['user']
    
)

@router.get(
    '/info',
    response_model=GetUserInfoResponseSchema,
    status_code=status.HTTP_200_OK,
    description='user info',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_user_info_handler(
    scheme: GetUserInfoRequestSchema,
    container = Depends(init_container)
):
    '''User info'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        user, *_ = await mediator.handle_query(
            GetUserInfoQuery(
                token=scheme.token
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    return GetUserInfoResponseSchema.from_entity(user)


@router.post(
    '/change/email',
    response_model=ChangeEmailResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Change email',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def login_user_handler(
    scheme: ChangeEmailRequestSchema, 
    container=Depends(init_container)
):
    '''Change email'''
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        stat, *_ = await mediator.handle_command(
            ChangeEmailCommand(
                token=scheme.token,
                new_email=scheme.new_email
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    return ChangeEmailResponseSchema(status=stat)

@router.post(
    '/add/adress',
    response_model=AddAdressResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Add adress',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def login_user_handler(
    scheme: AddAdressRequestSchema, 
    container=Depends(init_container)
):
    '''Add adress'''
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        adress, *_ = await mediator.handle_command(
            AddAdressCommand(
                token=scheme.token,
                region=scheme.region,
                locality=scheme.locality,
                street=scheme.street,
                building=scheme.building
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    return AddAdressResponseSchema.from_entity(adress)
