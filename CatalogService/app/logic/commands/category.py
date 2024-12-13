

from dataclasses import dataclass

from logic.services.catalog import BaseCatalogService
from domain.entities.category import Category
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class AddCategoryCommand(BaseCommand):
    token: str
    parent_category: str
    category_name: str
    
    
@dataclass(frozen=True)
class AddCategoryCommandHandler(CommandHandler[AddCategoryCommand, Category]):

    catalog_service: BaseCatalogService    
    async def handle(self, command: AddCategoryCommand) -> Category:
        return await self.catalog_service.add_category(command.token, command.parent_category, command.category_name)
    
@dataclass(frozen=True)
class AddProductCommand(BaseCommand):
    token: str
    name: str
    category_name: str
    description: str
    price: float
    discount_percent: float
    
    
@dataclass(frozen=True)
class AddProductCommandHandler(CommandHandler[AddProductCommand, Category]):

    catalog_service: BaseCatalogService    
    async def handle(self, command: AddProductCommand) -> Category:
        return await self.catalog_service.add_product(
            command.token, command.name, command.category_name,
            command.description, command.price, command.discount_percent)
        
