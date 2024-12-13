

from datetime import datetime
from typing import List
from pydantic import BaseModel

from domain.entities.order import Order
from domain.entities.storage import Storage
from domain.entities.product import Product
from domain.entities.category import Category

class AddCategoryRequestScheme(BaseModel):
    token: str
    parent_category: str
    category_name: str
    
class AddCategoryResponseScheme(BaseModel):
    category_id: str
    category_name: str
    
    @classmethod
    def from_entity(cls, category: Category) -> 'AddCategoryResponseScheme':
        return AddCategoryResponseScheme(
            category_id=category.oid,
            category_name=category.category_name
        )

class AddProductRequestScheme(BaseModel):
    token: str
    name: str
    category_name: str
    description: str
    price: float
    discount_percent: float
    
        
class AddProductResponseScheme(BaseModel):
    product_id: str
    name: str
    salesman_id: str
    category_id: str
    description: str
    rating: float | None
    price: float
    discount_percent: float
    
    @classmethod
    def from_entity(cls, product: Product) -> 'AddProductResponseScheme':
        return AddProductResponseScheme(
            product_id=product.oid,
            name=product.name,
            salesman_id=product.salesman_id,
            category_id=product.category_id,
            description=product.description,
            rating=product.rating,
            price=product.price,
            discount_percent=product.discount_percent
        )


class GetProductsByCategoryRequestScheme(BaseModel):
    category_name: str

class GetProductByCategoryResponseScheme(BaseModel):
    product_id: str
    name: str
    salesman_id: str
    category_id: str
    description: str
    rating: float | None
    price: float
    discount_percent: float
     
class GetProductsByCategoryResponseScheme(BaseModel):
    data: List[GetProductByCategoryResponseScheme]
    
class AddStorageRequestScheme(BaseModel):
    token: str
    region: str
    locality: str
    street: str
    building: str
    
class AddStorageResponseScheme(BaseModel):
    storage_id: str
    region: str
    locality: str
    street: str
    building: str
    
    @classmethod
    def from_entity(cls, storage: Storage) -> 'AddStorageResponseScheme':
        return AddStorageResponseScheme(
            storage_id = storage.oid,
            region = storage.region,
            locality = storage.locality,
            street = storage.street,
            building = storage.building
        )

class AddProductCountToStorageRequestScheme(BaseModel):
    token: str
    product_id: str
    storage_id: str
    count: int

class AddProductCountToStorageResponseScheme(BaseModel):
    count: int
     
class TakeProductCountFromStorageRequestScheme(BaseModel):
    token: str
    product_id: str
    storage_id: str
    count: int
    
class TakeProductCountFromStorageResponseScheme(BaseModel):
    count: int

class GetProductBySalesmanRequestScheme(BaseModel):
    token: str

class GetProductBySalesmanResponseScheme(BaseModel):
    product_id: str
    name: str
    salesman_id: str
    category_id: str
    description: str
    rating: float | None
    price: float
    discount_percent: float
    count: int | None
    storage_id: str | None
    region: str | None
    locality: str | None
    street: str | None
    building: str | None

class GetProductsBySalesmanResponseScheme(BaseModel):
    data: List[GetProductBySalesmanResponseScheme]
    
    
    
class CreateOrderRequestScheme(BaseModel):
    token: str
    
class CreateOrderResponseScheme(BaseModel):
    order_id: str
    user_id: str
    time_created: datetime
    time_delivered: datetime | None
    status: str
    is_paid: bool
    
    
    @classmethod
    def from_entity(cls, order: Order) -> 'CreateOrderResponseScheme':
        return CreateOrderResponseScheme(
            order_id=order.oid,
            user_id=order.user_id,
            time_created=order.time_created,
            time_delivered=order.time_delivered,
            status=order.status,
            is_paid=order.is_paid
        )
        
class AddProductToOrderRequestScheme(BaseModel):
    token: str
    product_id: str
    count: int
    
class AddProductToOrderResponseScheme(BaseModel):
    status: str = "Added"
    
    
class GetOrderInfoRequestScheme(BaseModel):
    token: str
    order_id: str


class ProductResponseScheme(BaseModel):
    product_id: str
    name: str
    salesman_id: str
    category_id: str
    description: str
    rating: float | None
    price: float
    discount_percent: float
    count: int | None
    
    @classmethod
    def from_entity(cls, product: Product) -> 'ProductResponseScheme':
        return ProductResponseScheme(
            product_id=product.oid,
            name=product.name,
            salesman_id=product.salesman_id,
            category_id=product.category_id,
            description=product.description,
            rating=product.rating,
            price=product.price,
            discount_percent=product.discount_percent,
            count=product.count
        )
    
    

class GetOrderInfoResponseScheme(BaseModel):
    order_id: str
    user_id: str
    time_created: datetime
    time_delivered: datetime | None
    status: str
    is_paid: bool
    products: list[ProductResponseScheme]
    
    @classmethod
    def from_entity(cls, order: Order) -> 'GetOrderInfoResponseScheme':
        
        prods = []
        for product in order.products:
            prods.append(
                ProductResponseScheme.from_entity(product)
            )
        
        return GetOrderInfoResponseScheme(
            order_id=str(order.oid),
            user_id=str(order.user_id),
            time_created=order.time_created,
            time_delivered=order.time_delivered,
            status=order.status,
            is_paid=order.is_paid,
            products=prods
        )
    
    
class GetOrdersInfoRequestScheme(BaseModel):
    token: str
    limit: int
    
class GetOrdersInfoResponseScheme(BaseModel):
    data: List[GetOrderInfoResponseScheme]
    
    @classmethod
    def from_entity(cls, orders: List[Order]) -> 'GetOrdersInfoResponseScheme':
        d = []
        
        for order in orders:
            d.append(
                GetOrderInfoResponseScheme.from_entity(order)
            )
        
        return GetOrdersInfoResponseScheme(
            data=d
        )