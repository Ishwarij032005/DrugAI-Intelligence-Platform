"""
DrugAI — Tests for Predictions routes.
"""
import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_list_predictions(async_client: AsyncClient):
    response = await async_client.get("/api/v1/predictions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.anyio
async def test_predict_toxicity(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/predictions/toxicity",
        json={"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "toxicity" in data
    assert "breakdown" in data
    assert "predictionId" in data

@pytest.mark.anyio
async def test_predict_invalid_smiles(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/predictions/toxicity",
        json={"smiles": "INVALID_SMILES"}
    )
    assert response.status_code == 400
