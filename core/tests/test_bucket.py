from unittest.mock import AsyncMock

import pytest

from app.storage.bucket import BUCKET_NAME, create_object, delete_object, read_object

s3 = AsyncMock()
test_key = "tests/3ui83ej"
test_content = b"Hello world from s3 mock test"


@pytest.mark.asyncio
async def test_create_object():
    await create_object(s3, test_key, test_content)
    
    s3.put_object.assert_awaited_once_with(
        Bucket=BUCKET_NAME,
        Key=test_key,
        Body=test_content,
    )
    
@pytest.mark.asyncio
async def test_read_object():
    body = AsyncMock()
    body.read.return_value = test_content
    
    s3.get_object.return_value = {
        "Body": body,
    }
    
    result = await read_object(
        s3=s3,
        bucket_key=test_key,
    )
    
    assert result == test_content
    
    s3.get_object.assert_awaited_once_with(
        Bucket=BUCKET_NAME,
        Key=test_key,
    )
    
    body.read.assert_awaited_once()
    
    
@pytest.mark.asyncio
async def test_delete_object():
    await delete_object(
        s3=s3,
        bucket_key=test_key,
    )
    
    s3.delete_object.assert_awaited_once_with(
        Bucket=BUCKET_NAME,
        Key=test_key,
    )
