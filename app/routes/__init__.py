"""
API route modules.

Routers for sales CRUD and insights endpoints are organized here
and included into the main FastAPI application.
"""

from fastapi import APIRouter

from app.routes import sales

api_router = APIRouter()
api_router.include_router(sales.router)

__all__ = ["api_router"]


