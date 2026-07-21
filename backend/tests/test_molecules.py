"""
DrugAI — Tests for Molecules routes.
"""
import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_validate_molecule(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/molecules/validate",
        json={"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert "molecularWeight" in data

@pytest.mark.anyio
async def test_molecule_svg(async_client: AsyncClient):
    response = await async_client.get("/api/v1/molecules/C/structure.svg")
    assert response.status_code == 200
    assert "svg" in response.text.lower()
