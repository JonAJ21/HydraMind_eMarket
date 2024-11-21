from pydantic import BaseModel

from domain.entities.user import User

class AddUserRequestSchema(BaseModel):
    login: str
    password: str
    email: str
    role: str
    
class AddUserResponseSchema(BaseModel):
    oid: str
    login: str
    password: str
    email: str
    role: str
    
    @classmethod
    def from_entity(cls, user: User) -> 'AddUserResponseSchema':
        return AddUserResponseSchema(
            oid=user.oid,
            login=user.login.as_generic_type(),
            password=user.password.as_generic_type(),
            email=user.email.as_generic_type(),
            role=user.role.as_generic_type()
        )