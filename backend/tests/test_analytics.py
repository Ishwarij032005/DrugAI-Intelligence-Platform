"""
DrugAI — Tests for Analytics routes.
"""
import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_dashboard_stats(async_client: AsyncClient):
    response = await async_client.get("/api/v1/analytics/dashboard-stats")
    assert response.status_code == 200
    data = response.json()
    assert "totalPredictions" in data
    assert "avgAccuracy" in data

@pytest.mark.anyio
async def test_trend(async_client: AsyncClient):
    response = await async_client.get("/api/v1/analytics/trend?days=7")
    assert response.status_code == 200
    assert len(response.json()) == 7
