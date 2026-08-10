from app.config import settings

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase


engine: AsyncEngine = create_async_engine(
    settings.postgres_url,
    pool_size=settings.db_pool_size,            # Permanent connections in pool
    max_overflow=settings.db_max_overflow,      # Temporary connections during spikes
    pool_timeout=settings.db_pool_timeout,      # Wait time for connection
    pool_recycle=settings.db_pool_recycle,      # Prevent stale connection
    pool_pre_ping=True,                         # Verify connection before use
    echo=settings.db_echo,                      # If set true useful for debugging
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
        finally:
            await session.close()
    
class Base(DeclarativeBase):
    """
    Base class for all models using SQLAlechemy's 2.0 syntax.
    """
    pass

async def initialize_database() -> None:
    """
    Create table metadata in database if not exists.
    This uses a sync connection because the 'create_all' doesn't feature async yet.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 
