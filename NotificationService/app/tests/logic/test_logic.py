import pytest
from logic.commands.notification import AddNotificationCommand, AddNotificationCommandHandler
from logic.services.notification import BaseNotificationService
from domain.entities.notification import Notification
from unittest.mock import AsyncMock

@pytest.fixture
def mock_notification_service():
    return AsyncMock(spec=BaseNotificationService)

@pytest.mark.asyncio
async def test_add_notification_command_handler(mock_notification_service):
    command = AddNotificationCommand(user_id="user123", text="New notification")

    handler = AddNotificationCommandHandler(notification_service=mock_notification_service)

    mock_notification_service.add_notification.return_value = Notification(
        oid="notif1",
        user_id="user123",
        text="New notification",
        is_readed=False
    )

    notification = await handler.handle(command)

    mock_notification_service.add_notification.assert_awaited_once_with("user123", "New notification")

    assert notification.user_id == "user123"
    assert notification.text == "New notification"
    assert notification.is_readed is False
