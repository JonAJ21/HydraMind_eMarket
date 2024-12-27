
from pydantic import BaseModel


class AddCategoryRequestScheme(BaseModel):
    parent_category: str
    category_name: str
    
class AddProductRequestScheme(BaseModel):
    name: str
    category_name: str
    description: str
    price: float
    discount_percent: float
    
class AddStorageRequestScheme(BaseModel):
    region: str
    locality: str
    street: str
    building: str
    