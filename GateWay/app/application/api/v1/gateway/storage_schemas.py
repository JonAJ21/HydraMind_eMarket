
from pydantic import BaseModel


class AddStorageRequestScheme(BaseModel):
    region: str
    locality: str
    street: str
    building: str
    
class AddProductToStorageRequestScheme(BaseModel):
    product_id: str
    storage_id: str
    count: int
    
class TakeProductFromStorageRequestScheme(BaseModel):
    product_id: str
    storage_id: str
    count: int
    

