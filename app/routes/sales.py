"""
Sales CRUD API routes.

Exposes RESTful endpoints for managing sales data, using the service layer to
interact with the database and Pydantic schemas for validation/serialization.
"""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.sale import (
    ItemsSoldResponse,
    RevenueResponse,
    SaleCreate,
    SaleResponse,
    SaleUpdate,
)
from app.services import sales_service

router = APIRouter(prefix="/api/sales", tags=["Sales"])


@router.post(
    "",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new sale record",
)
async def create_sale_endpoint(
    payload: SaleCreate,
    db: AsyncSession = Depends(get_db),
) -> SaleResponse:
    sale = await sales_service.create_sale(db, payload)
    return SaleResponse(**sale)


@router.get(
    "",
    response_model=List[SaleResponse],
    summary="List sales with optional filters",
)
async def list_sales_endpoint(
    start_date: Optional[date] = Query(None, description="Filter sales from this date (inclusive)"),
    end_date: Optional[date] = Query(None, description="Filter sales up to this date (inclusive)"),
    product_name: Optional[str] = Query(None, description="Filter sales for a specific product"),
    db: AsyncSession = Depends(get_db),
) -> List[SaleResponse]:
    filters = {
        "start_date": start_date,
        "end_date": end_date,
        "product_name": product_name,
    }
    # Remove None values to avoid unnecessary filters
    filters = {key: value for key, value in filters.items() if value is not None}
    sales = await sales_service.get_sales(db, filters)
    return [SaleResponse(**sale) for sale in sales]


@router.get(
    "/{sale_id}",
    response_model=SaleResponse,
    summary="Retrieve a sale by ID",
)
async def get_sale_endpoint(
    sale_id: int,
    db: AsyncSession = Depends(get_db),
) -> SaleResponse:
    sale = await sales_service.get_sale_by_id(db, sale_id)
    if sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return SaleResponse(**sale)


@router.put(
    "/{sale_id}",
    response_model=SaleResponse,
    summary="Update a sale by ID",
)
async def update_sale_endpoint(
    sale_id: int,
    payload: SaleUpdate,
    db: AsyncSession = Depends(get_db),
) -> SaleResponse:
    sale = await sales_service.update_sale(db, sale_id, payload)
    if sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return SaleResponse(**sale)


@router.delete(
    "/{sale_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a sale by ID",
)
async def delete_sale_endpoint(
    sale_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    deleted = await sales_service.delete_sale(db, sale_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    # 204 No Content responses should not include a body
    return None


@router.get(
    "/analytics/revenue",
    response_model=RevenueResponse,
    summary="Get total revenue",
)
async def get_total_revenue_endpoint(
    start_date: Optional[date] = Query(None, description="Filter sales from this date (inclusive)"),
    end_date: Optional[date] = Query(None, description="Filter sales up to this date (inclusive)"),
    product_name: Optional[str] = Query(None, description="Filter sales for a specific product"),
    db: AsyncSession = Depends(get_db),
) -> RevenueResponse:
    """
    Calculate total revenue (sum of quantity * price) for sales.
    Supports optional filtering by date range and product name.
    """
    filters = {
        "start_date": start_date,
        "end_date": end_date,
        "product_name": product_name,
    }
    # Remove None values to avoid unnecessary filters
    filters = {key: value for key, value in filters.items() if value is not None}
    total_revenue = await sales_service.get_total_revenue(db, filters)
    return RevenueResponse(total_revenue=total_revenue)


@router.get(
    "/analytics/items-sold",
    response_model=ItemsSoldResponse,
    summary="Get total items sold",
)
async def get_total_items_sold_endpoint(
    start_date: Optional[date] = Query(None, description="Filter sales from this date (inclusive)"),
    end_date: Optional[date] = Query(None, description="Filter sales up to this date (inclusive)"),
    product_name: Optional[str] = Query(None, description="Filter sales for a specific product"),
    db: AsyncSession = Depends(get_db),
) -> ItemsSoldResponse:
    """
    Calculate total items sold (sum of quantities) for sales.
    Supports optional filtering by date range and product name.
    """
    filters = {
        "start_date": start_date,
        "end_date": end_date,
        "product_name": product_name,
    }
    # Remove None values to avoid unnecessary filters
    filters = {key: value for key, value in filters.items() if value is not None}
    total_items = await sales_service.get_total_items_sold(db, filters)
    return ItemsSoldResponse(total_items_sold=total_items)


