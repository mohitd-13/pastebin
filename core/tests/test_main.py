import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(app_client: AsyncClient):
    response = await app_client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Pastebin"}

@pytest.mark.asyncio
async def test_health(app_client: AsyncClient):
    response = await app_client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "Healthy"}
