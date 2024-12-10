
from dataclasses import dataclass

from logic.services.user import BaseUserService
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class ChangeEmailCommand(BaseCommand):
    token: str
    new_email: str
    
@dataclass(frozen=True)
class ChangeEmailCommandHandler(CommandHandler[ChangeEmailCommand, bool]):
    user_service: BaseUserService
   
    async def handle(self, command: ChangeEmailCommand) -> bool:
        return await self.user_service.change_email(command.token, command.new_email)