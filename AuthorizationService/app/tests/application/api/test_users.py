from httpx import Response

from fastapi import FastAPI, status
from fastapi.testclient import TestClient

import pytest

@pytest.mark.asyncio
async def test_add_user_succes(
    app: FastAPI,
    client: TestClient
):
    url = app.url_path_for('add_user_handler')
    response: Response = client.post(
        url=url, 
        json={
            "login": "string",
            "password": "string",
            "email": "string",
            "role": "ADMIN"
        }
    )
    assert response.is_success
    json_data = response.json()
    assert json_data['role'] == 'ADMIN'
    
@pytest.mark.asyncio
async def test_add_user_fail_login_too_long(
    app: FastAPI,
    client: TestClient
):
    url = app.url_path_for('add_user_handler')
    
    response: Response = client.post(
        url=url, 
        json={
            "login": "s" * 300,
            "password": "string",
            "email": "string",
            "role": "ADMIN"
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()
    json_data = response.json()
    assert json_data['detail']['error']
    