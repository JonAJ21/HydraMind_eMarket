from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException

from logic.init import init_container
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from application.api.user.schemas import AddUserRequestSchema, AddUserResponseSchema
from logic.commands.user import AddUserCommand
from logic.mediator import Mediator
# from application.api.dependencies.containers import container

router = APIRouter(
    tags=['User'],
)

@router.post(
    '/',
    response_model=AddUserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Add new user to DB',
    responses={
        status.HTTP_200_OK: {'model': AddUserRequestSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def add_user_handler(schema: AddUserRequestSchema, container=Depends(init_container)):
    '''Add new user to DB'''
    
    mediator: Mediator = container.resolve(Mediator)
    

    try:
        user, *_ = await mediator.handle_command(
            AddUserCommand(
                login=schema.login,
                password=schema.password,
                email=schema.email,
                role=schema.role
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
        
    return AddUserResponseSchema.from_entity(user)
    

# @router.post('/p')
# def f():
#     return