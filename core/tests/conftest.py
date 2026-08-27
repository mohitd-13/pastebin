from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.dependencies import get_db, get_s3_bucket_session
from app.main import app
from app.models import Bin


@pytest.fixture
def mock_s3() -> AsyncMock:
    """A fake S3 bucket session."""
    return AsyncMock()

@pytest.fixture
def mock_db() -> AsyncMock:
    """A fake database session."""
    return AsyncMock()

@pytest_asyncio.fixture
async def app_client(mock_s3: AsyncMock, mock_db: AsyncMock) -> AsyncGenerator[AsyncClient, None]:
    """A test client for the FastAPI app."""

    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_s3_bucket_session] = lambda: mock_s3

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport,
            base_url="http://test"
        ) as client:
            yield client
    finally:
        app.dependency_overrides.clear()

@pytest.fixture
def paste_data() -> Bin:
    return Bin(
        id="abcd1234",
        created_at="2024-01-01T00:00:00Z",
        expiry_at="2024-01-02T00:00:00Z",
        size_bytes=1024
    )
