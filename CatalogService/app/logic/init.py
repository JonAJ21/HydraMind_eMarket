
from functools import lru_cache
from punq import Container, Scope

from infrastructure.repositories.order import BaseOrderRepository, PostgreOrderRepository
from logic.commands.order import AddProductToOrderCommand, AddProductToOrderCommandHandler, ChangeOrderStatusCommand, ChangeOrderStatusCommandHandler, CreateOrderCommand, CreateOrderCommandHandler
from logic.queries.order import GetOrderInfoQuery, GetOrderInfoQueryHandler, GetOrdersInfoQuery, GetOrdersInfoQueryHandler
from logic.services.order import BaseOrderService, RESTOrderService
from logic.queries.storage import GetProductsInfoBySalesmanQuery, GetProductsInfoBySalesmanQueryHandler
from logic.commands.storage import AddProductCountToStorageCommand, AddProductCountToStorageCommandHandler, AddStorageCommand, AddStorageCommandHandler, TakeProductCountFromStorageCommand, TakeProductCountFromStorageCommandHandler
from logic.services.storage import BaseStorageService, RESTStorageService
from infrastructure.repositories.storage import BaseStorageRepository, PostgreStorageRepository
from logic.queries.catalog import GetCategoriesQuery, GetCategoriesQueryHandler, GetProductsByCategoryQuery, GetProductsByCategoryQueryHandler
from logic.commands.category import AddCategoryCommand, AddCategoryCommandHandler, AddProductCommand, AddProductCommandHandler
from infrastructure.repositories.catalog import BaseCatalogRepository, PostgreCatalogRepository
from logic.services.catalog import BaseCatalogService, RESTCatalogService
from logic.mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()

def _init_container() -> Container:
    container = Container()
    
    container.register(BaseCatalogService, RESTCatalogService, scope=Scope.singleton)
    container.register(BaseStorageService, RESTStorageService, scope=Scope.singleton)
    container.register(BaseOrderService, RESTOrderService, scope=Scope.singleton)
    
    
    container.register(AddCategoryCommandHandler)
    container.register(AddProductCommandHandler)
    container.register(GetProductsByCategoryQueryHandler)
    container.register(GetCategoriesQueryHandler)
    container.register(AddStorageCommandHandler)
    container.register(AddProductCountToStorageCommandHandler)
    container.register(TakeProductCountFromStorageCommandHandler)
    container.register(GetProductsInfoBySalesmanQueryHandler)
    container.register(CreateOrderCommandHandler)
    container.register(AddProductToOrderCommandHandler)
    container.register(GetOrderInfoQueryHandler)
    container.register(GetOrdersInfoQueryHandler)
    container.register(ChangeOrderStatusCommandHandler)
    
    
    def init_mediator():
        mediator = Mediator()
        
        mediator.register_command(
            AddCategoryCommand,
            [container.resolve(AddCategoryCommandHandler)]
        )
        
        mediator.register_command(
            AddProductCommand,
            [container.resolve(AddProductCommandHandler)]
        )
        
        mediator.register_query(
            GetProductsByCategoryQuery,
            [container.resolve(GetProductsByCategoryQueryHandler)]
        )
        
        mediator.register_query(
            GetCategoriesQuery,
            [container.resolve(GetCategoriesQueryHandler)]
        )
        
        mediator.register_command(
            AddStorageCommand,
            [container.resolve(AddStorageCommandHandler)]
        )
        
        mediator.register_command(
            AddProductCountToStorageCommand,
            [container.resolve(AddProductCountToStorageCommandHandler)]
        )
        
        mediator.register_command(
            TakeProductCountFromStorageCommand,
            [container.resolve(TakeProductCountFromStorageCommandHandler)]
        )
        
        mediator.register_query(
            GetProductsInfoBySalesmanQuery,
            [container.resolve(GetProductsInfoBySalesmanQueryHandler)]
        )
        
        mediator.register_command(
            CreateOrderCommand,
            [container.resolve(CreateOrderCommandHandler)]
        )
        
        mediator.register_command(
            AddProductToOrderCommand,
            [container.resolve(AddProductToOrderCommandHandler)]
        )
        
        mediator.register_query(
            GetOrderInfoQuery,
            [container.resolve(GetOrderInfoQueryHandler)]
        )
        
        mediator.register_query(
            GetOrdersInfoQuery,
            [container.resolve(GetOrdersInfoQueryHandler)]
        )
        
        mediator.register_command(
            ChangeOrderStatusCommand,
            [container.resolve(ChangeOrderStatusCommandHandler)]
        )
        
        

        return mediator
    
    container.register(Mediator, factory=init_mediator)
    
    def init_postgre_catalog_repository():
        return PostgreCatalogRepository()    
        
    container.register(BaseCatalogRepository, factory=init_postgre_catalog_repository, scope=Scope.singleton)
    
    def init_postgre_storage_repository():
        return PostgreStorageRepository()
    
    container.register(BaseStorageRepository, factory=init_postgre_storage_repository, scope=Scope.singleton)
    
    def init_postgre_order_repository():
        return PostgreOrderRepository()
    
    container.register(BaseOrderRepository, factory=init_postgre_order_repository, scope=Scope.singleton)
        
    
    return container
    
