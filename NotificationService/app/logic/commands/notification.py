from dataclasses import dataclass

from logic.services.notification import BaseNotificationService
from domain.entities.notification import Notification
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class AddNotificationCommand(BaseCommand):
    user_id: str
    text: str
    
@dataclass(frozen=True)
class AddNotificationCommandHandler(CommandHandler[AddNotificationCommand, Notification]):
    notification_service: BaseNotificationService
   
    async def handle(self, command: AddNotificationCommand) -> Notification:
        return await self.notification_service.add_notification(command.user_id, command.text)