"""
Pydantic v2 schemas for Sale model validation and serialization.

This module defines request/response schemas for the Sale API endpoints,
including validation rules for data integrity.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SaleBase(BaseModel):
    """
    Base schema with common fields for Sale.

    This is used as a base for both create and update schemas.
    """

    product_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the product sold",
        examples=["Laptop", "Mouse", "Keyboard"],
    )
    quantity: int = Field(
        ...,
        gt=0,
        description="Number of items sold (must be greater than 0)",
        examples=[5, 10, 25],
    )
    price: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Price per item (must be >= 0)",
        examples=[99.99, 150.00, 29.50],
    )
    sale_date: date = Field(
        ...,
        description="Date of the sale (YYYY-MM-DD format)",
        examples=["2024-01-15", "2024-11-27"],
    )


class SaleCreate(SaleBase):
    """
    Schema for creating a new sale record.

    All fields are required and validated according to business rules.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "product_name": "Laptop",
                "quantity": 2,
                "price": 999.99,
                "sale_date": "2024-11-27",
            }
        }
    )


class SaleUpdate(BaseModel):
    """
    Schema for updating an existing sale record.

    All fields are optional - only provided fields will be updated.
    Validation rules apply to provided fields.
    """

    product_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Name of the product sold",
        examples=["Laptop", "Mouse", "Keyboard"],
    )
    quantity: Optional[int] = Field(
        None,
        gt=0,
        description="Number of items sold (must be greater than 0)",
        examples=[5, 10, 25],
    )
    price: Optional[Decimal] = Field(
        None,
        ge=0,
        decimal_places=2,
        description="Price per item (must be >= 0)",
        examples=[99.99, 150.00, 29.50],
    )
    sale_date: Optional[date] = Field(
        None,
        description="Date of the sale (YYYY-MM-DD format)",
        examples=["2024-01-15", "2024-11-27"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "product_name": "Updated Laptop",
                "quantity": 3,
                "price": 1099.99,
                "sale_date": "2024-11-28",
            }
        }
    )


class SaleResponse(SaleBase):
    """
    Schema for returning sale records in API responses.

    Includes all base fields plus auto-generated fields (id, timestamps).
    Uses from_attributes=True to work with SQLAlchemy ORM models.
    """

    id: int = Field(..., description="Unique identifier for the sale record")
    created_at: datetime = Field(..., description="Timestamp when the record was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when the record was last updated"
    )

    model_config = ConfigDict(
        from_attributes=True,  # Enables ORM mode for SQLAlchemy models
        json_schema_extra={
            "example": {
                "id": 1,
                "product_name": "Laptop",
                "quantity": 2,
                "price": 999.99,
                "sale_date": "2024-11-27",
                "created_at": "2024-11-27T10:30:00",
                "updated_at": "2024-11-27T10:30:00",
            }
        },
    )

