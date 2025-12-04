"""
Service layer for Sale CRUD operations.

Encapsulates all business logic and database interactions for sales, ensuring
that routes/controllers can remain thin and focused on HTTP concerns.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, Iterable, List, Optional

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleResponse, SaleUpdate


def _serialize_sale(sale: Sale) -> Dict[str, Any]:
    """
    Convert a SQLAlchemy Sale instance into a clean dictionary using the
    SaleResponse schema for consistent serialization.
    """
    return SaleResponse.model_validate(sale).model_dump()


async def create_sale(db: AsyncSession, sale_data: SaleCreate) -> Dict[str, Any]:
    """
    Create a new sale record.
    """
    sale = Sale(**sale_data.model_dump())
    db.add(sale)
    await db.commit()
    await db.refresh(sale)
    return _serialize_sale(sale)


async def get_sales(
    db: AsyncSession,
    filters: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve sales with optional filtering by date range and product name.

    Supported filters:
        - start_date (date): inclusive lower bound for sale_date
        - end_date (date): inclusive upper bound for sale_date
        - product_name (str): exact match on product name
    """
    filters = filters or {}
    query = select(Sale).order_by(Sale.sale_date.desc(), Sale.id.desc())

    start_date: Optional[date] = filters.get("start_date")
    end_date: Optional[date] = filters.get("end_date")
    product_name: Optional[str] = filters.get("product_name")

    if start_date:
        query = query.where(Sale.sale_date >= start_date)
    if end_date:
        query = query.where(Sale.sale_date <= end_date)
    if product_name:
        query = query.where(Sale.product_name == product_name)

    result = await db.execute(query)
    sales: Iterable[Sale] = result.scalars().all()
    return [_serialize_sale(sale) for sale in sales]


async def get_sale_by_id(db: AsyncSession, sale_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single sale by its ID.
    """
    result = await db.execute(select(Sale).where(Sale.id == sale_id))
    sale = result.scalar_one_or_none()
    if sale is None:
        return None
    return _serialize_sale(sale)


async def update_sale(
    db: AsyncSession,
    sale_id: int,
    sale_data: SaleUpdate,
) -> Optional[Dict[str, Any]]:
    """
    Update an existing sale record with the provided data.
    """
    result = await db.execute(select(Sale).where(Sale.id == sale_id))
    sale = result.scalar_one_or_none()
    if sale is None:
        return None

    update_payload = sale_data.model_dump(exclude_unset=True)
    for field, value in update_payload.items():
        setattr(sale, field, value)

    await db.commit()
    await db.refresh(sale)
    return _serialize_sale(sale)


async def delete_sale(db: AsyncSession, sale_id: int) -> bool:
    """
    Delete a sale record by its ID.

    Returns:
        bool: True if a record was deleted, False otherwise.
    """
    result = await db.execute(select(Sale).where(Sale.id == sale_id))
    sale = result.scalar_one_or_none()
    if sale is None:
        return False

    await db.delete(sale)
    await db.commit()
    return True


async def get_total_revenue(
    db: AsyncSession,
    filters: Optional[Dict[str, Any]] = None,
) -> Decimal:
    """
    Calculate total revenue (sum of quantity * price) for sales.

    Supported filters:
        - start_date (date): inclusive lower bound for sale_date
        - end_date (date): inclusive upper bound for sale_date
        - product_name (str): exact match on product name

    Returns:
        Decimal: Total revenue across matching sales
    """
    filters = filters or {}
    query = select(func.sum(Sale.quantity * Sale.price))

    start_date: Optional[date] = filters.get("start_date")
    end_date: Optional[date] = filters.get("end_date")
    product_name: Optional[str] = filters.get("product_name")

    if start_date:
        query = query.where(Sale.sale_date >= start_date)
    if end_date:
        query = query.where(Sale.sale_date <= end_date)
    if product_name:
        query = query.where(Sale.product_name == product_name)

    result = await db.execute(query)
    total = result.scalar()
    # Return 0 if no sales match the filters
    return Decimal("0.00") if total is None else Decimal(str(total))


async def get_total_items_sold(
    db: AsyncSession,
    filters: Optional[Dict[str, Any]] = None,
) -> int:
    """
    Calculate total items sold (sum of quantities) for sales.

    Supported filters:
        - start_date (date): inclusive lower bound for sale_date
        - end_date (date): inclusive upper bound for sale_date
        - product_name (str): exact match on product name

    Returns:
        int: Total number of items sold across matching sales
    """
    filters = filters or {}
    query = select(func.sum(Sale.quantity))

    start_date: Optional[date] = filters.get("start_date")
    end_date: Optional[date] = filters.get("end_date")
    product_name: Optional[str] = filters.get("product_name")

    if start_date:
        query = query.where(Sale.sale_date >= start_date)
    if end_date:
        query = query.where(Sale.sale_date <= end_date)
    if product_name:
        query = query.where(Sale.product_name == product_name)

    result = await db.execute(query)
    total = result.scalar()
    # Return 0 if no sales match the filters
    return 0 if total is None else int(total)


