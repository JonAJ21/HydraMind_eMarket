
from fastapi import APIRouter, Depends, HTTPException, status


from logic.queries.order import GetOrderInfoQuery, GetOrdersInfoQuery
from logic.commands.order import AddProductToOrderCommand, CreateOrderCommand
from logic.queries.storage import GetProductsInfoBySalesmanQuery
from logic.commands.storage import AddProductCountToStorageCommand, AddStorageCommand, TakeProductCountFromStorageCommand
from logic.queries.catalog import GetProductsByCategoryQuery
from logic.commands.category import AddCategoryCommand, AddProductCommand
from application.api.v1.catalog.schemas import AddCategoryRequestScheme, AddCategoryResponseScheme, AddProductCountToStorageRequestScheme, AddProductCountToStorageResponseScheme, AddProductRequestScheme, AddProductResponseScheme, AddProductToOrderRequestScheme, AddProductToOrderResponseScheme, AddStorageRequestScheme, AddStorageResponseScheme, CreateOrderRequestScheme, CreateOrderResponseScheme, GetOrderInfoRequestScheme, GetOrderInfoResponseScheme, GetOrdersInfoRequestScheme, GetOrdersInfoResponseScheme, GetProductByCategoryResponseScheme, GetProductBySalesmanRequestScheme, GetProductBySalesmanResponseScheme, GetProductsByCategoryRequestScheme, GetProductsByCategoryResponseScheme, GetProductsBySalesmanResponseScheme, TakeProductCountFromStorageRequestScheme, TakeProductCountFromStorageResponseScheme
from domain.exceptions.base import ApplicationException
from logic.mediator import Mediator
from logic.init import init_container
from application.api.v1.schemas import ErrorSchema



router = APIRouter(
    tags=['catalog']
    
)



@router.post(
    '/add/category',
    response_model=AddCategoryResponseScheme,
    status_code=status.HTTP_201_CREATED,
    description='Add category',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def add_category_handler(
    scheme: AddCategoryRequestScheme, 
    container=Depends(init_container)
):
    '''Add category'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        category, *_ = await mediator.handle_command(
            AddCategoryCommand(
                token=scheme.token,
                parent_category=scheme.parent_category,
                category_name=scheme.category_name
            ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    return AddCategoryResponseScheme.from_entity(category)


@router.post(
    '/add/product',
    response_model=AddProductResponseScheme,
    status_code=status.HTTP_201_CREATED,
    description='Add product',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def add_product_handler(
    scheme: AddProductRequestScheme, 
    container=Depends(init_container)
):
    '''Add category'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        product, *_ = await mediator.handle_command(
            AddProductCommand(
                token=scheme.token,
                name=scheme.name,
                category_name=scheme.category_name,
                description=scheme.description,
                price=scheme.price,
                discount_percent=scheme.discount_percent,
            ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    return AddProductResponseScheme.from_entity(product)

@router.get(
    '/get/category/products',
    response_model=GetProductsByCategoryResponseScheme,
    status_code=status.HTTP_200_OK,
    description='Get products by category name',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_products_by_category_handler(
    scheme: GetProductsByCategoryRequestScheme,
    container = Depends(init_container)
):
    '''Get products by category'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        products, *_ = await mediator.handle_query(
            GetProductsByCategoryQuery(
                category_name=scheme.category_name
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    data = []
    for product in products:
        schema = GetProductByCategoryResponseScheme(
            product_id=product.oid,
            name=product.name,
            salesman_id=product.salesman_id,
            category_id=product.category_id,
            description=product.description,
            rating=product.rating,
            price=product.price,
            discount_percent=product.discount_percent
        )
        data.append(schema)
    
    return GetProductsByCategoryResponseScheme(data=data)

@router.post(
    '/add/storage',
    response_model=AddStorageResponseScheme,
    status_code=status.HTTP_201_CREATED,
    description='Add storage',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def add_storage_handler(
    scheme: AddStorageRequestScheme, 
    container=Depends(init_container)
):
    '''Add storage'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        storage, *_ = await mediator.handle_command(
            AddStorageCommand(
                token=scheme.token,
                region = scheme.region,
                locality = scheme.locality,
                street = scheme.street,
                building = scheme.building
            ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    return AddStorageResponseScheme.from_entity(storage)


@router.post(
    '/add/storage/product',
    response_model=AddProductCountToStorageResponseScheme,
    status_code=status.HTTP_201_CREATED,
    description='Add product to storage',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def add_product_to_storage_handler(
    scheme: AddProductCountToStorageRequestScheme, 
    container=Depends(init_container)
):
    '''Add product to storage'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        count, *_ = await mediator.handle_command(
            AddProductCountToStorageCommand(
                token=scheme.token,
                product_id=scheme.product_id,
                storage_id=scheme.storage_id,
                count=scheme.count
            ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    return AddProductCountToStorageResponseScheme(count=count)

@router.post(
    '/take/storage/product',
    response_model=TakeProductCountFromStorageResponseScheme,
    status_code=status.HTTP_201_CREATED,
    description='Take product from storage',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def take_product_from_storage_handler(
    scheme: TakeProductCountFromStorageRequestScheme, 
    container=Depends(init_container)
):
    '''Take product from storage'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        count, *_ = await mediator.handle_command(
            TakeProductCountFromStorageCommand(
                token=scheme.token,
                product_id=scheme.product_id,
                storage_id=scheme.storage_id,
                count=scheme.count
            ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    return TakeProductCountFromStorageResponseScheme(count=count)



@router.get(
    '/get/salesman/products',
    response_model=GetProductsBySalesmanResponseScheme,
    status_code=status.HTTP_200_OK,
    description='Get salesman products',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_prodycts_by_salesman_handler(
    scheme: GetProductBySalesmanRequestScheme,
    container = Depends(init_container)
):
    '''Get salesman products'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        elements, *_ = await mediator.handle_query(
            GetProductsInfoBySalesmanQuery(
                token=scheme.token
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    data = []
    # print(elements)
    for elem in elements:
        schema = GetProductBySalesmanResponseScheme(
            product_id=elem.product.oid,
            name=elem.product.name,
            salesman_id=elem.product.salesman_id,
            category_id=elem.product.category_id,
            description=elem.product.description,
            rating=elem.product.rating,
            price=elem.product.price,
            discount_percent=elem.product.discount_percent,
            count=elem.psc.count,
            storage_id=elem.storage.oid,
            region=elem.storage.region,
            locality=elem.storage.locality,
            street=elem.storage.street,
            building=elem.storage.building
        )
        data.append(schema)
    
    return GetProductsBySalesmanResponseScheme(data=data)


#==================================================================

@router.post(
    '/create/order',
    response_model=CreateOrderResponseScheme,
    status_code=status.HTTP_201_CREATED,
    description='Create order',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def create_order_handler(
    scheme: CreateOrderRequestScheme, 
    container=Depends(init_container)
):
    '''Create order'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        order, *_ = await mediator.handle_command(
            CreateOrderCommand(
                token=scheme.token,
            ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    return CreateOrderResponseScheme.from_entity(order)

@router.post(
    '/add/order/product',
    response_model=AddProductToOrderResponseScheme,
    status_code=status.HTTP_201_CREATED,
    description='AddProductToOrder',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def add_product_to_order_handler(
    scheme: AddProductToOrderRequestScheme, 
    container=Depends(init_container)
):
    '''Add product to order'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        order, *_ = await mediator.handle_command(
            AddProductToOrderCommand(
                token=scheme.token,
                product_id=scheme.product_id,
                count=scheme.count
            ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    return AddProductToOrderResponseScheme()





@router.get(
    '/get/order/info',
    response_model=GetOrderInfoResponseScheme,
    status_code=status.HTTP_200_OK,
    description='Get order info',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_order_info_handler(
    scheme: GetOrderInfoRequestScheme,
    container = Depends(init_container)
):
    '''Get order info'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        order, *_ = await mediator.handle_query(
            GetOrderInfoQuery(
                token=scheme.token,
                order_id=scheme.order_id
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    return GetOrderInfoResponseScheme.from_entity(order)

@router.get(
    '/get/orders/info',
    response_model=GetOrdersInfoResponseScheme,
    status_code=status.HTTP_200_OK,
    description='Get orders info',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_orders_info_handler(
    scheme: GetOrdersInfoRequestScheme,
    container = Depends(init_container)
):
    '''Get order info'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        orders, *_ = await mediator.handle_query(
            GetOrdersInfoQuery(
                token=scheme.token,
                limit=scheme.limit
        ))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': exception.message}
        )
    
    return GetOrdersInfoResponseScheme.from_entity(orders)


