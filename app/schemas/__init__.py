"""
Pydantic v2 schemas for request and response models.

These schemas will be used to validate and serialize sales data
and analytics responses exposed via the API.
"""

from app.schemas.sale import (
    ItemsSoldResponse,
    RevenueResponse,
    SaleCreate,
    SaleResponse,
    SaleUpdate,
)

__all__ = [
    "SaleCreate",
    "SaleUpdate",
    "SaleResponse",
    "RevenueResponse",
    "ItemsSoldResponse",
]

