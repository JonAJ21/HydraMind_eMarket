from dataclasses import dataclass

from logic.services.auth import BaseAuthService
from logic.services.jwt import TokenInfo
from logic.commands.base import BaseCommand, CommandHandler

@dataclass(frozen=True)
class RefreshTokenCommand(BaseCommand):
    token: str
    
@dataclass(frozen=True)
class RefreshTokenCommandHandler(CommandHandler[RefreshTokenCommand, TokenInfo]):
    auth_service: BaseAuthService    
    
    async def handle(self, command: RefreshTokenCommand) -> TokenInfo:
        return await self.auth_service.refresh(command.token)
        