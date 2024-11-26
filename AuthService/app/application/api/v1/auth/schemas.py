from pydantic import BaseModel, ConfigDict

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