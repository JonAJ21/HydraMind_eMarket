from dataclasses import dataclass

from logic.services.user import BaseUserService
from logic.commands.base import BaseCommand, CommandHandler



@dataclass(frozen=True)
class ChangeUserRoleCommand(BaseCommand):
    token: str
    login: str
    new_role: str
    
@dataclass(frozen=True)
class ChangeUserRoleCommandHandler(CommandHandler[ChangeUserRoleCommand, bool]):
    user_service: BaseUserService
   
    async def handle(self, command: ChangeUserRoleCommand) -> bool:
        return await self.user_service.change_user_role(command.token, command.login, command.new_role)