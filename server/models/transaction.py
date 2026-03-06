from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class Transaction(BaseModel):
    """A recorded purchase event for a single item at a specific store."""

    transaction_id: UUID
    item_id: UUID
    price: Annotated[float, Field(gt=0, description="Price must be strictly greater than 0.")]
    quantity: float
    store_name: str
    timestamp: datetime

    @field_validator("store_name")
    @classmethod
    def validate_store_name(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("store_name must not be empty or whitespace-only.")
        return value.strip()

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: float) -> float:
        if value <= 0:
            raise ValueError(
                f"quantity must be greater than 0, received {value}."
            )
        return value
