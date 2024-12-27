
from pydantic import BaseModel


class AddUserAdressRequestScheme(BaseModel):
    region: str
    locality: str
    street: str
    building: str