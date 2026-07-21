"""
DrugAI — Tests for Models routes.
"""
import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_list_models(async_client: AsyncClient):
    response = await async_client.get("/api/v1/models/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.anyio
async def test_get_model(async_client: AsyncClient):
    response = await async_client.get("/api/v1/models/m1")
    assert response.status_code == 200
    assert response.json()["id"] == "m1"
