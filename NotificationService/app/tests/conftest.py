import pytest
from logic.mediator import Mediator
from logic.services.notification import BaseNotificationService
from unittest.mock import AsyncMock

@pytest.fixture
def mock_mediator():
    return AsyncMock(spec=Mediator)

@pytest.fixture
def mock_notification_service():
    return AsyncMock(spec=BaseNotificationService)

@pytest.fixture(scope='session', autouse=True)
async def setup_test_database():
    yield

@pytest.fixture
async def test_client():
    from fastapi.testclient import TestClient
    from application.api.v1.main import create_app

    app = create_app()
    client = TestClient(app)

    yield client
