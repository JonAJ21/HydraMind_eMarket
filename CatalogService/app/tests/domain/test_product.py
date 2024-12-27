import pytest
from domain.entities.product import Product
from domain.entities.base import BaseEntity
from domain.entities.storage import Storage

def test_product_equality():
    product1 = Product(
        name="Product A",
        salesman_id="123",
        category_id="cat1",
        description="Description of Product A",
        price=100.0,
        discount_percent=10.0
    )
    product2 = Product(
        name="Product A",
        salesman_id="123",
        category_id="cat1",
        description="Description of Product A",
        price=100.0,
        discount_percent=10.0
    )

    assert (product1.name == product2.name and
            product1.salesman_id == product2.salesman_id and
            product1.category_id == product2.category_id and
            product1.description == product2.description and
            product1.price == product2.price and
            product1.discount_percent == product2.discount_percent)

def test_product_hash():
    product1 = Product(
        name="Product A",
        salesman_id="123",
        category_id="cat1",
        description="Description of Product A",
        price=100.0,
        discount_percent=10.0
    )
    product2 = Product(
        name="Product A",
        salesman_id="123",
        category_id="cat1",
        description="Description of Product A",
        price=100.0,
        discount_percent=10.0
    )
    
    assert hash((product1.name, product1.salesman_id, product1.category_id, product1.description,
                 product1.price, product1.discount_percent)) == \
           hash((product2.name, product2.salesman_id, product2.category_id, product2.description,
                 product2.price, product2.discount_percent))


@pytest.mark.parametrize(
    "region, locality, street, building",
    [
        ("Region A", "Locality A", "Street A", "Building A"),
        ("Region B", "Locality B", "Street B", "Building B"),
    ]
)
def test_storage(region, locality, street, building):
    storage = Storage(
        region=region,
        locality=locality,
        street=street,
        building=building
    )
    
    assert storage.region == region
    assert storage.locality == locality
    assert storage.street == street
    assert storage.building == building
