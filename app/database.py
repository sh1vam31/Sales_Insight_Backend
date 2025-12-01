from collections.abc import AsyncGenerator
import os

from sqlalchemy.engine import make_url
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

url = make_url(raw_database_url)

# If we're using PostgreSQL without an explicit async driver, upgrade it
# to use asyncpg so that SQLAlchemy's asyncio extension works.
if url.drivername in ("postgresql", "postgres"):
    url = url.set(drivername="postgresql+asyncpg")

DATABASE_URL = str(url)

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


