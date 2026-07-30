from fastapi import Depends
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


engine: AsyncEngine = create_async_engine(
    settings.postgres_url,
    pool_size=5,                # Permanent connections in pool
    max_overflow=10,            # Temporary connections during spikes
    pool_pre_ping=True,         # Verify connection before use
    echo=True                   # print logs on terminal useful when debugging
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,     # Keep data accessible after commit
    autocommit=False,           # Require explicit commits
    autoflush=False,            # Manual control over flushing    
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function for FastAPI endpoints.
    Yields a database session and ensures proper cleanup
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
    
class Base(DeclarativeBase):
    """
    Base class for all models using SQLAlechemy's 2.0 syntax.
    """
    pass
