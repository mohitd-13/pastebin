from aiobotocore.client import AioBaseClient
from botocore.exceptions import ClientError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Bin
from app.storage.bucket import create_object, delete_object, read_object
from app.utils import generate_random_string

MAX_RETRIES_ATTEMPTS = 10

async def insert_new_record_with_retries(content: str, db: AsyncSession, s3: AioBaseClient) -> Bin:
    encoded_text = content.encode()
    size_in_bytes = len(encoded_text)

    if size_in_bytes > 1024 * 1024:
        raise ValueError("Paste Content size should be lesser then 1MB")

    for attempt in range(MAX_RETRIES_ATTEMPTS):
        unique_str = generate_random_string()

        new_record = Bin(
            id=unique_str,
            size_bytes=size_in_bytes,
        )
        bucket_key = f"pastes/{unique_str}"

        try:
            db.add(new_record)
            await db.commit()

        except IntegrityError:
            await db.rollback()
            if attempt == MAX_RETRIES_ATTEMPTS - 1:
                raise RuntimeError(
                    f"Could not create a new record after {MAX_RETRIES_ATTEMPTS} attempts."
                )
            continue

        try:
            await create_object(s3, bucket_key, encoded_text)
        except ClientError:
            await db.delete(new_record)
            await db.commit()

            raise RuntimeError("Failed to store paste Data")

        return new_record

    raise RuntimeError("Unreachable")

async def read_content_from_bucket(paste_id: str, s3: AioBaseClient) -> str:
    bucket_key = f"pastes/{paste_id}"
    encoded_text = await read_object(s3, bucket_key)
    return encoded_text.decode()

async def read_content_metadata(paste_id: str, db: AsyncSession) -> Bin | None:
    stmt = select(Bin).where(Bin.id == paste_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def delete_paste_record(paste_id: str, db: AsyncSession, s3: AioBaseClient) -> bool:
    bucket_key = f"pastes/{paste_id}"
    stmt = select(Bin).where(Bin.id == paste_id)
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()
    if not record:
        return False
    await delete_object(s3, bucket_key)
    await db.delete(record)
    await db.commit()
    return True
