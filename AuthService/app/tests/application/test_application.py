import pytest
from httpx import AsyncClient
from fastapi import status
from application.api.v1.main import create_app
from unittest.mock import AsyncMock

from application.api.v1.auth.schemas import RegisterUserRequestSchema, LoginUserRequestSchema

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_mediator(mocker):
    return mocker.patch("application.api.v1.auth.handlers.Mediator")
