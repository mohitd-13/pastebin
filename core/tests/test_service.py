from unittest.mock import AsyncMock, patch

import pytest
from botocore.exceptions import ClientError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.service import insert_new_record_with_retries

text_content = "Hello world from service mock test"

@pytest.mark.asyncio
async def test_insert_new_record_success():
    s3 = AsyncMock()
    db = AsyncMock(spec=AsyncSession)
    result = await insert_new_record_with_retries(text_content, db, s3)
    
    assert result.id
    assert result.size_bytes == len(text_content.encode())
    
    db.add.assert_called_once_with(result)
    db.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_insert_new_record_s3_failure():
    s3 = AsyncMock()
    db = AsyncMock(spec=AsyncSession)
    
    s3_error = ClientError(
        {
            "Error": {
                "Code": "InternalError",
                "Message": "S3 upload failed",
            }
        },
        "PutObject",
    )

    with patch(
        "app.service.create_object",
        new_callable=AsyncMock,
    ) as mock_create_object:

        mock_create_object.side_effect = s3_error

        with pytest.raises(
            RuntimeError,
            match="Failed to store paste Data",
        ):
            await insert_new_record_with_retries(
                content=text_content,
                db=db,
                s3=s3,
            )

    db.add.assert_called_once()
    assert db.commit.await_count == 2

    db.delete.assert_awaited_once()

    record = db.delete.await_args.args[0]

    assert record.id
    assert record.size_bytes == len(text_content.encode())

    mock_create_object.assert_awaited_once_with(
        s3,
        f"pastes/{record.id}",
        text_content.encode(),
    )
    
@pytest.mark.asyncio
async def test_insert_new_record_id_collision():
    db = AsyncMock(spec=AsyncSession)
    s3 = AsyncMock()

    commit_error = IntegrityError(
        statement="INSERT INTO bin",
        params={},
        orig=Exception("duplicate key"),
    )

    with (
        patch(
            "app.service.generate_random_string",
            side_effect=["abc123", "xyz789"],
        ),
        patch(
            "app.service.create_object",
            new_callable=AsyncMock,
        ) as mock_create_object,
    ):
        db.commit.side_effect = [commit_error, None]

        result = await insert_new_record_with_retries(
            content=text_content,
            db=db,
            s3=s3,
        )

    assert result.id == "xyz789"
    assert result.size_bytes == len(text_content.encode())

    assert db.add.call_count == 2
    assert db.commit.await_count == 2

    db.rollback.assert_awaited_once()

    mock_create_object.assert_awaited_once_with(
        s3,
        "pastes/xyz789",
        text_content.encode(),
    )    