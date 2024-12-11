
from fastapi import APIRouter, Depends, HTTPException, status

from logic.commands.role import ChangeUserRoleCommand
from logic.queries.get_adresses import GetAdressesQuery
from logic.commands.adress import AddAdressCommand, DeleteAdressCommand
from logic.commands.email import ChangeEmailCommand
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from logic.init import init_container
from logic.mediator import Mediator
from logic.queries.get_user import GetUserInfoQuery
from application.api.v1.schemas import ErrorSchema
from application.api.v1.user.schemas import AddAdressRequestSchema, AddAdressResponseSchema, ChangeEmailRequestSchema, ChangeEmailResponseSchema, ChangeUserRoleRequestSchema, ChangeUserRoleResponseSchema, DeleteAdressRequestSchema, DeleteAdressResponseSchema, GetAdressResponseSchema, GetAdressesRequestSchema, GetAdressesResponseSchema, GetUserInfoRequestSchema, GetUserInfoResponseSchema


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


@router.put(
    '/change/email',
    response_model=ChangeEmailResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Change email',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def change_user_email_handler(
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
async def add_user_adress_handler(
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

#====================================================================

@router.get(
    '/get/adresses',
    response_model=GetAdressesResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Get adresses',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_user_adresses_handler(
    scheme: GetAdressesRequestSchema, 
    container=Depends(init_container)
):
    '''Add adress'''
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        adresses, *_ = await mediator.handle_query(
            GetAdressesQuery(
                token=scheme.token,
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    data = []
    for adress in adresses:
        schema = GetAdressResponseSchema(
            adress_id=adress.oid,
            region=adress.region.as_generic_type(),
            locality=adress.locality.as_generic_type(),
            street=adress.street.as_generic_type(),
            building=adress.building.as_generic_type()
        )
        data.append(schema)
    
    
    return GetAdressesResponseSchema(data=data)


@router.put(
    '/delete/adress',
    response_model=DeleteAdressResponseSchema,
    status_code=status.HTTP_200_OK,
    description='Delete adress',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def delete_user_adress_handler(
    scheme: DeleteAdressRequestSchema, 
    container=Depends(init_container)
):
    '''Add adress'''
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        stat, *_ = await mediator.handle_command(
            DeleteAdressCommand(
                token=scheme.token,
                adress_id=scheme.adress_id
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    
    
    return DeleteAdressResponseSchema(status=stat)



@router.put(
    '/change/role',
    response_model=ChangeUserRoleResponseSchema,
    status_code=status.HTTP_200_OK,
    description='Change role',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def change_user_role_handler(
    scheme: ChangeUserRoleRequestSchema, 
    container=Depends(init_container)
):
    '''Add adress'''
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        stat, *_ = await mediator.handle_command(
            ChangeUserRoleCommand(
                token=scheme.token,
                login=scheme.login,
                new_role=scheme.new_role        
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    
    
    return DeleteAdressResponseSchema(status=stat)