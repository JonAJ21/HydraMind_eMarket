from dataclasses import dataclass

from domain.entities.adress import Adress
from logic.services.user import BaseUserService
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class AddAdressCommand(BaseCommand):
    token: str
    region: str
    locality: str
    street: str
    building: str
    
@dataclass(frozen=True)
class AddAdressCommandHandler(CommandHandler[AddAdressCommand, Adress]):
    user_service: BaseUserService
   
    async def handle(self, command: AddAdressCommand) -> Adress:
        return await self.user_service.add_user_adress(
            command.token, command.region, command.locality,
            command.street, command.building)