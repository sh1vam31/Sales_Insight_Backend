from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# NOTE:
# For initial development, we use a local SQLite database.
# This can be replaced with a production-grade database URL
# (e.g., PostgreSQL) via environment variables or settings module later.
DATABASE_URL = "sqlite:///./sales_insights.db"

# `connect_args` is required for SQLite when using a file-based database.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Dependency that provides a transactional database session.

    Yields:
        SQLAlchemy Session object.

    Ensures the session is closed after the request is handled.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


