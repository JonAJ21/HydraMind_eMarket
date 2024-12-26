import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from unittest.mock import AsyncMock

from application.api.v1.main import create_app

@pytest.fixture
def app() -> FastAPI:
    """Создает экземпляр приложения FastAPI для тестов."""
    return create_app()

@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    """Создает клиента для отправки HTTP запросов к приложению."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_mediator(mocker):
    """Мокирует Mediator для тестов."""
    return mocker.patch("application.api.v1.auth.handlers.Mediator")