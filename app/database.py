from collections.abc import AsyncGenerator
import os

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

# NOTE:
# We default to a local SQLite database for development.
# In production (e.g., Render), a DATABASE_URL environment variable
# can be provided (typically pointing to PostgreSQL).
DEFAULT_SQLITE_URL = "sqlite+aiosqlite:///./sales_insights.db"

raw_database_url = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

# Convert PostgreSQL URLs to use asyncpg driver for async SQLAlchemy
# Render provides URLs like: postgres://user:pass@host/db
# We need: postgresql+asyncpg://user:pass@host/db
if raw_database_url.startswith("postgres://"):
    # Replace postgres:// with postgresql+asyncpg://
    DATABASE_URL = raw_database_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif raw_database_url.startswith("postgresql://") and "+asyncpg" not in raw_database_url:
    # Replace postgresql:// with postgresql+asyncpg:// if not already present
    DATABASE_URL = raw_database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    # Keep as-is (SQLite or already has async driver)
    DATABASE_URL = raw_database_url

# SQLAlchemy 2.0 style declarative base
Base = declarative_base()

# Global async engine and session factory.
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def init_db() -> None:
    """
    Initialize the database on application startup.

    - Imports all ORM models so their metadata is registered.
    - Creates all tables if they do not exist.
    """
    # Import models so that they are registered with SQLAlchemy's metadata.
    # This local import avoids circular dependencies at import time.
    from app import models  # noqa: F401  # pylint: disable=unused-import

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an AsyncSession.

    Usage example:
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            # AsyncSession context manager handles close/rollback/commit,
            # but we explicitly close for clarity.
            await session.close()


