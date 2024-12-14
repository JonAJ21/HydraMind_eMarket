from dataclasses import dataclass

from domain.entities.order import Order
from logic.commands.base import BaseCommand, CommandHandler
from logic.services.order import BaseOrderService


@dataclass(frozen=True)
class CreateOrderCommand(BaseCommand):
    token: str

@dataclass(frozen=True)
class CreateOrderCommandHandler(CommandHandler[CreateOrderCommand, Order]):
    order_service: BaseOrderService    
    
    async def handle(self, command: CreateOrderCommand) -> Order:
        return await self.order_service.create_order(command.token)
    
@dataclass(frozen=True)
class AddProductToOrderCommand(BaseCommand):
    token: str
    product_id: str
    count: int

@dataclass(frozen=True)
class AddProductToOrderCommandHandler(CommandHandler[AddProductToOrderCommand, None]):
    order_service: BaseOrderService    
    
    async def handle(self, command: AddProductToOrderCommand) -> None:
        return await self.order_service.add_product_to_order(command.token, command.product_id, command.count)
    
@dataclass(frozen=True)
class ChangeOrderStatusCommand(BaseCommand):
    token: str
    order_id: str
    status: int

@dataclass(frozen=True)
class ChangeOrderStatusCommandHandler(CommandHandler[ChangeOrderStatusCommand, None]):
    order_service: BaseOrderService    
    
    async def handle(self, command: ChangeOrderStatusCommand) -> None:
        return await self.order_service.change_order_status(command.token, command.order_id, command.status)
    