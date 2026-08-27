from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from app.models import Bin


@pytest.mark.asyncio
async def test_read_paste_success(
    app_client: AsyncClient,
    mock_s3: AsyncMock,
):
    paste_id = "abc123"
    paste_content = "Hello from test"

    with patch(
        "app.routers.pastes.read_content_from_bucket",
        new_callable=AsyncMock,
        return_value=paste_content,
    ) as mock_read:
        response = await app_client.get(f"/pastes/{paste_id}")

    assert response.status_code == 200
    assert response.json() == paste_content

    mock_read.assert_awaited_once_with(paste_id, mock_s3)

@pytest.mark.asyncio
async def test_read_paste_not_found(
    app_client: AsyncClient,
    mock_s3: AsyncMock,
):
    paste_id="does-not-exist"

    with patch(
        "app.routers.pastes.read_content_from_bucket",
        new_callable=AsyncMock,
        return_value=None,
    ) as mock_read:
        response = await app_client.get(f"/pastes/{paste_id}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Paste Content not found"}

        mock_read.assert_awaited_once_with(paste_id, mock_s3)

@pytest.mark.asyncio
async def test_delete_paste_success(
    app_client: AsyncClient,
    mock_s3: AsyncMock,
    mock_db: AsyncMock,
):
    paste_id = "abcd1234"

    with patch(
        "app.routers.pastes.delete_paste_record",
        new_callable=AsyncMock,
        return_value=True,
    ) as mock_delete:
        response = await app_client.delete(f"/pastes/{paste_id}")

    assert response.status_code == 204
    assert response.content == b""

    mock_delete.assert_awaited_once_with(paste_id, mock_db, mock_s3)

@pytest.mark.asyncio
async def test_delete_paste_not_found(
    app_client: AsyncClient,
    mock_s3: AsyncMock,
    mock_db: AsyncMock,
):
    paste_id = "does-not-exist"

    with patch(
        "app.routers.pastes.delete_paste_record",
        new_callable=AsyncMock,
        return_value=False,
    ) as mock_delete:
        response = await app_client.delete(f"/pastes/{paste_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Paste not found"
    }

    mock_delete.assert_awaited_once_with(paste_id, mock_db, mock_s3)

@pytest.mark.asyncio
async def test_read_paste_metadata_success(
    app_client: AsyncClient,
    mock_db: AsyncMock,
    paste_data: Bin,
):
    with patch(
        "app.routers.pastes.read_content_metadata",
        new_callable=AsyncMock,
        return_value=paste_data,
    ) as mock_get:
        response = await app_client.get(f"/pastes/metadata/{paste_data.id}")
        data = response.json()

    assert response.status_code == 200
    assert data["id"] == paste_data.id
    assert data["created_at"] == paste_data.created_at
    assert data["expiry_at"] == paste_data.expiry_at
    assert data["size_bytes"] == paste_data.size_bytes

    mock_get.assert_awaited_once_with(paste_data.id, mock_db)

@pytest.mark.asyncio
async def test_read_paste_metadata_not_found(
    app_client: AsyncClient,
    mock_db: AsyncMock,
):
    paste_id = "abcd1234"

    with patch(
        "app.routers.pastes.read_content_metadata",
        new_callable=AsyncMock,
        return_value=None,
    ) as mock_get:
        response = await app_client.get(f"/pastes/metadata/{paste_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Paste metadata not found"
    }

    mock_get.assert_awaited_once_with(paste_id, mock_db)

@pytest.mark.asyncio
async def test_create_paste_success(
    app_client: AsyncClient,
    mock_db: AsyncMock,
    mock_s3: AsyncMock,
    paste_data: Bin,
):

    paste_content = "Hello, World from pytest!"

    with patch(
        "app.routers.pastes.insert_new_record_with_retries",
        new_callable=AsyncMock,
        return_value=paste_data,
    ) as mock_post:
        response = await app_client.post(
            "/pastes/",
            json={"content": paste_content},
        )
        data = response.json()

    assert response.status_code == 201
    assert data["id"] == paste_data.id
    assert data["created_at"] == paste_data.created_at
    assert data["expiry_at"] == paste_data.expiry_at
    assert data["size_bytes"] == paste_data.size_bytes

    mock_post.assert_awaited_once_with(paste_content, mock_db, mock_s3)

@pytest.mark.asyncio
async def test_create_paste_invalid(
    app_client: AsyncClient,
):
    response = await app_client.post(
        "/pastes/",
        json={},
    )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_paste_service_failure(
    app_client: AsyncClient,
    mock_db: AsyncMock,
    mock_s3: AsyncMock,
):
    paste_content = "Hello, World from pytest!"

    with (
        patch(
            "app.routers.pastes.insert_new_record_with_retries",
            new_callable=AsyncMock,
            side_effect=RuntimeError("Failed to store paste Data"),
        ) as mock_post,
        pytest.raises(
            RuntimeError,
            match="Failed to store paste Data",
        ),
    ):
        _ = await app_client.post(
            "/pastes/",
            json={"content": paste_content},
        )

    mock_post.assert_awaited_once_with(paste_content, mock_db, mock_s3)
