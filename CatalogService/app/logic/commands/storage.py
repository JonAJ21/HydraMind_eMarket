from dataclasses import dataclass

from domain.entities.storage import Storage
from logic.services.storage import BaseStorageService
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class AddStorageCommand(BaseCommand):
    token: str
    region: str
    locality: str
    street: str
    building: str
    
    
@dataclass(frozen=True)
class AddStorageCommandHandler(CommandHandler[AddStorageCommand, Storage]):
    storage_service: BaseStorageService    
    
    async def handle(self, command: AddStorageCommand) -> Storage:
        return await self.storage_service.add_storage(
            command.token, command.region, command.locality,
            command.street, command.building
        )
        
@dataclass(frozen=True)
class AddProductCountToStorageCommand(BaseCommand):
    token: str
    product_id: str
    storage_id: str
    count: int
    
    
@dataclass(frozen=True)
class AddProductCountToStorageCommandHandler(CommandHandler[AddProductCountToStorageCommand, int]):
    storage_service: BaseStorageService    
    
    async def handle(self, command: AddProductCountToStorageCommand) -> int:
        return await self.storage_service.add_product_to_storage(
            command.token, command.product_id, command.storage_id, command.count
        )
        
@dataclass(frozen=True)
class TakeProductCountFromStorageCommand(BaseCommand):
    token: str
    product_id: str
    storage_id: str
    count: int
    
    
@dataclass(frozen=True)
class TakeProductCountFromStorageCommandHandler(CommandHandler[TakeProductCountFromStorageCommand, int]):
    storage_service: BaseStorageService    
    
    async def handle(self, command: TakeProductCountFromStorageCommand) -> int:
        return await self.storage_service.take_product_count_from_storage(
            command.token, command.product_id, command.storage_id, command.count
        )