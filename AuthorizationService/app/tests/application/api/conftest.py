from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from tests.fixtures import init_dummy_container
from logic.init import init_container
from application.api.main import create_app


@pytest.fixture
def app() -> TestClient:
    app = create_app()
    app.dependency_overrides[init_container] = init_dummy_container
    return app
    

@pytest.fixture
def client(app: FastAPI) -> TestClient:     
    return TestClient(app=app)