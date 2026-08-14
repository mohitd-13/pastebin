from collections.abc import AsyncGenerator
from typing import Annotated

from aiobotocore.client import AioBaseClient
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function for FastAPI endpoints
    Yields a database session and ensures proper cleanup
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

def get_s3_bucket_session(request: Request) -> AioBaseClient:
    """
    Return the S3 bucket session from the request app state
    Started during FastAPI startup
    """
    return request.app.state.s3

DBSessionDep = Annotated[AsyncSession, Depends(get_db)]
S3SessionDep = Annotated[AioBaseClient, Depends(get_s3_bucket_session)]
