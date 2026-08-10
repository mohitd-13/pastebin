from core.app.models import Bin
from core.app.utils import generate_random_string
from core.app.storage.bucket import (
    create_object, read_object, delete_object
)

from boto3.exceptions import S3UploadFailedError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

MAX_RETRIES_ATTEMPTS = 10

async def insert_new_content_with_retries(content: str, db: AsyncSession) -> Bin | None:
    encoded_text = content.encode()
    size_in_bytes = len(encoded_text)
    
    if size_in_bytes > 1024:
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
            try:
                create_object(bucket_key, encoded_text)
            except S3UploadFailedError:
                raise RuntimeError(f"Failed to upload content")
            return new_record
        
        except IntegrityError:
            await db.rollback()
            if attempt == MAX_RETRIES_ATTEMPTS - 1:
                raise RuntimeError(
                    f"Could not create a new record after {MAX_RETRIES_ATTEMPTS} attempts."
                )
            continue
        
    raise RuntimeError("Unreachable")

async def read_content_from_bucket(paste_id: str) -> str:
    bucket_key = f"pastes/{paste_id}"
    encoded_text = read_object(bucket_key)
    return encoded_text.decode()

async def read_content_metadata(paste_id: str, db: AsyncSession) -> Bin | None:
    stmt = select(Bin).where(Bin.id == paste_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def delete_content(paste_id: str, db: AsyncSession) -> bool:
    bucket_key = f"pastes/{paste_id}"
    delete_object(bucket_key)
    stmt = select(Bin).where(Bin.id == paste_id)
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()
    if not record:
        return False
    await db.delete(record)
    await db.commit()
    return True
    
            
