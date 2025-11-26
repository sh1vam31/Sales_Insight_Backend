from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Use this to initialize shared resources (DB, clients, etc.)
    and clean them up on shutdown.
    """
    # TODO: Initialize resources here (e.g., DB connection pool)
    yield
    # TODO: Clean up resources here


app = FastAPI(
    title="Sales Insights Backend",
    description=(
        "Backend service for managing sales data and generating insights "
        "such as total revenue, total items sold, and best-selling products."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Health"])
async def root():
    """
    Health check / root endpoint.

    Used by clients or monitoring to verify that the backend is running.
    """
    return {"message": "Sales Insights Backend Running"}


def get_app() -> FastAPI:
    """
    Application factory for ASGI servers and testing.
    """
    return app


