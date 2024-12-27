import pytest
from unittest.mock import AsyncMock
from logic.services.user import BaseUserService


@pytest.fixture
def mock_user_service():
    """Фикстура для мокированного сервиса пользователя."""
    mock_service = AsyncMock(BaseUserService)
    return mock_service
