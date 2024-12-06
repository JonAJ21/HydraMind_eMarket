from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jwt import InvalidTokenError


from logic.commands.refresh import RefreshTokenCommand
from logic.queries.user import GetUserInfoQuery
from logic.commands.login import LoginUserCommand
from domain.exceptions.base import ApplicationException
from logic.commands.register import RegisterUserCommand
from logic.mediator import Mediator
from logic.init import init_container
from application.api.v1.schemas import ErrorSchema
from application.api.v1.auth.schemas import GetUserInfoRequestSchema, GetUserInfoResponseSchema, LoginUserRequestSchema, LoginUserResponseSchema, RefreshTokenRequestSchema, RefreshTokenResponseSchema, RegisterUserRequestSchema, RegisterUserResponseSchema

http_bearer = HTTPBearer(auto_error=False)

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl='/auth/login'
)

router = APIRouter(
    tags=['Auth'],
    dependencies=[Depends(http_bearer)]
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
    # container = await init_container()
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        user, *_ = await mediator.handle_command(
            RegisterUserCommand(
                login=schema.login,
                password=schema.password,
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
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def login_user_handler(
    # username: Annotated[str, Form()],
    # password: Annotated[str, Form()],
    scheme: LoginUserRequestSchema, 
    container=Depends(init_container)
):
    '''Login user'''
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        tokenInfo, *_ = await mediator.handle_command(
            LoginUserCommand(
                login=scheme.login,#.username,
                password=scheme.password
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
        
    return LoginUserResponseSchema.from_entity(tokenInfo)

@router.post(
    '/refresh',
    response_model=RefreshTokenResponseSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    description='Refresh token',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def auth_refresh_jwt_handler(
    # credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    scheme: RefreshTokenRequestSchema,
    container=Depends(init_container),
    ):
    '''Refresh token'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        tokenInfo, *_ = await mediator.handle_command(
            RefreshTokenCommand(
                token=scheme.token
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    except AttributeError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'error': 'Did not authorize'}
        )
        
    return RefreshTokenResponseSchema.from_entity(tokenInfo)



@router.get(
    '/user/info',
    response_model=GetUserInfoResponseSchema,
    status_code=status.HTTP_200_OK,
    description='User info',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_user_info_handler(
    scheme: GetUserInfoRequestSchema,
    container = Depends(init_container)
    # token: str = Depends(oauth2_bearer)
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
    except InvalidTokenError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid token error. {exception}'
        )
        
    return GetUserInfoResponseSchema.from_entity(user)
    