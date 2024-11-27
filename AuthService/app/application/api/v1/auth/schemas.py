from datetime import datetime
from tokenize import TokenInfo
from pydantic import BaseModel

from domain.entities.user import User


class RegisterUserRequestSchema(BaseModel):
    login: str
    password: str
    role: str
    
class RegisterUserResponseSchema(BaseModel):
    oid: str
    login: str
    password: str
    email: str | None
    role: str
    active: bool
    
    @classmethod
    def from_entity(cls, user: User) -> 'RegisterUserResponseSchema':
        if user.email is None:
            return RegisterUserResponseSchema(
            oid=user.oid,
            login=user.login.as_generic_type(),
            password=user.password.as_generic_type(),
            email=user.email,
            role=user.role.as_generic_type(),
            active=user.active
        )
        return RegisterUserResponseSchema(
            oid=user.oid,
            login=user.login.as_generic_type(),
            password=user.password.as_generic_type(),
            email=user.email.as_generic_type(),
            role=user.role.as_generic_type(),
            active=user.active
        )
        
class LoginUserRequestSchema(BaseModel):
    login: str
    password: str
    
class LoginUserResponseSchema(BaseModel):
    access_token: str
    token_type: str
    
    @classmethod
    def from_entity(cls, tokenInfo: TokenInfo) -> 'LoginUserResponseSchema':
        return LoginUserResponseSchema(
            access_token=tokenInfo.access_token,
            token_type=tokenInfo.token_type
        )
    

class GetUserInfoRequestSchema(BaseModel):
    ...
    
class GetUserInfoResponseSchema(BaseModel):
    oid: str
    login: str
    password: str
    email: str | None
    role: str
    active: bool
    
    @classmethod
    def from_entity(cls, user: User) -> 'GetUserInfoResponseSchema':
        if user.email is None:
            return GetUserInfoResponseSchema(
            oid=user.oid,
            login=user.login.as_generic_type(),
            password=user.password.as_generic_type(),
            email=user.email,
            role=user.role.as_generic_type(),
            active=user.active
        )
        return GetUserInfoResponseSchema(
            oid=user.oid,
            login=user.login.as_generic_type(),
            password=user.password.as_generic_type(),
            email=user.email.as_generic_type(),
            role=user.role.as_generic_type(),
            active=user.active
        )
    
       
