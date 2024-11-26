from fastapi import APIRouter, Depends, HTTPException, status

from domain.exceptions.base import ApplicationException
from logic.commands.auth import RegisterUserCommand
from logic.mediator import Mediator
from logic.init import init_container
from application.api.v1.schemas import ErrorSchema
from application.api.v1.auth.schemas import RegisterUserRequestSchema, RegisterUserResponseSchema


router = APIRouter(
    tags=['Auth']
)

@router.post(
    '/',
    response_model=RegisterUserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Register new user',
    responses={
        status.HTTP_200_OK: {'model': RegisterUserRequestSchema },
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def register_user_handler(schema: RegisterUserRequestSchema, container=Depends(init_container)):
    '''Register new user'''
    
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        user, *_ = await mediator.handle_command(
            RegisterUserCommand(
                login=schema.login,
                password=schema.password,
                role=schema.role
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
        
    return RegisterUserResponseSchema.from_entity(user)