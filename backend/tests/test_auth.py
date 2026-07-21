"""
DrugAI — Tests for Auth routes.
"""
import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_register_user(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "New User",
            "email": "new@drugai.com",
            "password": "Password123"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.anyio
async def test_login(async_client: AsyncClient, test_user):
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@drugai.com",
            "password": "Password123"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

@pytest.mark.anyio
async def test_login_invalid(async_client: AsyncClient, test_user):
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@drugai.com",
            "password": "wrongpassword"
        },
    )
    assert response.status_code == 401
