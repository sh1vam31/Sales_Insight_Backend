from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

import os

# NOTE:
# For initial development, we use a local SQLite database via aiosqlite.
# For production deployment (e.g., Render), use PostgreSQL via DATABASE_URL env var.
# Render automatically provides DATABASE_URL for PostgreSQL instances.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./sales_insights.db")

# Render provides postgres:// URLs, but SQLAlchemy requires postgresql://
# This handles the conversion automatically
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# SQLAlchemy 2.0 style declarative base
Base = declarative_base()

# Global async engine and session factory.
# In a larger app you might construct these from a settings module.
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


