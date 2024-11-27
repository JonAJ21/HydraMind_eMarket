from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jwt import InvalidTokenError


from logic.queries.user import GetUserInfoQuery
from logic.commands.login import LoginUserCommand
from domain.exceptions.base import ApplicationException
from logic.commands.register import RegisterUserCommand
from logic.mediator import Mediator
from logic.init import init_container
from application.api.v1.schemas import ErrorSchema
from application.api.v1.auth.schemas import GetUserInfoRequestSchema, GetUserInfoResponseSchema, LoginUserRequestSchema, LoginUserResponseSchema, RegisterUserRequestSchema, RegisterUserResponseSchema

# http_bearer = HTTPBearer()
oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl='/auth/login'
)

router = APIRouter(
    tags=['Auth']
)

@router.post(
    '/register',
    response_model=RegisterUserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Register new user',
    responses={
        # status.HTTP_200_OK: {'model': RegisterUserRequestSchema },
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

@router.post(
    '/login',
    response_model=LoginUserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Login user',
    responses={
        # status.HTTP_200_OK: {'model': LoginUserRequestSchema },
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def login_user_handler(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    container=Depends(init_container)):
    '''Login user'''
    print(username, password)
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        tokenInfo, *_ = await mediator.handle_command(
            LoginUserCommand(
                login=username,
                password=password
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
        
    return LoginUserResponseSchema.from_entity(tokenInfo)



@router.get(
    '/user/info',
    response_model=GetUserInfoResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='User info',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_user_info_handler(
    # schema: GetUserInfoRequestSchema,
    container = Depends(init_container),
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    token: str = Depends(oauth2_bearer)
):
    '''User info'''
    
    # try: 
    #     token = credentials.credentials
    # except InvalidTokenError as exception:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail={'error': exception.message}
    #     )
        
    mediator: Mediator = container.resolve(Mediator)
    try:
        user, *_ = await mediator.handle_query(
            GetUserInfoQuery(
                token=token#credentials.credentials
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    except InvalidTokenError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid token error. {exception}'
        )
        
        
    return GetUserInfoResponseSchema.from_entity(user)
    