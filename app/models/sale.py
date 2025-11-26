"""
SQLAlchemy ORM model for Sale records.

This model represents a single sales transaction with product information,
quantity, price, and date. It includes indexes for efficient querying.
"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Sale(Base):
    """
    Sale model representing a sales transaction.

    Attributes:
        id: Primary key, auto-incrementing integer
        product_name: Name of the product sold (required)
        quantity: Number of items sold (must be > 0)
        price: Price per item (must be >= 0)
        sale_date: Date of the sale
        created_at: Timestamp when the record was created
        updated_at: Timestamp when the record was last updated
    """

    __tablename__ = "sales"

    # Primary key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    # Product information
    product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    # Quantity with constraint: must be > 0
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Price with constraint: must be >= 0
    # Using Numeric with 10 digits and 2 decimal places for currency
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # Sale date
    sale_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Table-level constraints
    __table_args__ = (
        # Ensure quantity is positive
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        # Ensure price is non-negative
        CheckConstraint("price >= 0", name="check_price_non_negative"),
        # Composite index on (sale_date, product_name) for efficient filtering
        Index("idx_sale_date_product", "sale_date", "product_name"),
    )

    def __repr__(self) -> str:
        """String representation of the Sale model."""
        return (
            f"<Sale(id={self.id}, product_name='{self.product_name}', "
            f"quantity={self.quantity}, price={self.price}, "
            f"sale_date={self.sale_date})>"
        )

