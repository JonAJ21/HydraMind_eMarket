
from dataclasses import Field
from typing import List
from pydantic import BaseModel

from domain.entities.adress import Adress
from domain.entities.user import User


class GetUserInfoRequestSchema(BaseModel):
    token: str
       
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

class ChangeEmailRequestSchema(BaseModel):
    token: str
    new_email: str
     
class ChangeEmailResponseSchema(BaseModel):
    status: bool
    
    
class AddAdressRequestSchema(BaseModel):
    token: str
    region: str
    locality: str
    street: str
    building: str
    
class AddAdressResponseSchema(BaseModel):
    adress_id: str
    user_id: str
    region: str
    locality: str
    street: str
    building: str
    
    @classmethod
    def from_entity(cls, adress: Adress) -> 'AddAdressResponseSchema':
        return AddAdressResponseSchema(
            adress_id=adress.oid,
            user_id=adress.user_id,
            region=adress.region.as_generic_type(),
            locality=adress.locality.as_generic_type(),
            street=adress.street.as_generic_type(),
            building=adress.building.as_generic_type()
        )
        
class GetAdressesRequestSchema(BaseModel):
    token: str

class GetAdressResponseSchema(BaseModel):
    adress_id: str
    region: str
    locality: str
    street: str
    building: str
    
    
class GetAdressesResponseSchema(BaseModel):
    data: List[GetAdressResponseSchema]
    
    # @classmethod
    # def from_entity(cls, adresses: List[Adress]) -> 'GetAdressesResponseSchema':
        
    #     for adress in adresses:
    #         schema = GetAdressResponseSchema(
    #             adress_id=adress.oid,
    #             region=adress.region.as_generic_type(),
    #             locality=adress.locality.as_generic_type(),
    #             street=adress.street.as_generic_type(),
    #             building=adress.building.as_generic_type()
    #         )
    #         data.append(schema)
    #     print(data)
    #     return data