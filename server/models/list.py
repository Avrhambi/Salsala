from datetime import datetime
from typing import List as PyList
from uuid import UUID

from pydantic import BaseModel, field_validator

from server.models.item import Item


class ShoppingList(BaseModel):
    """
    A collaborative shopping list shared between one or more users.
    Named ShoppingList to avoid shadowing Python's built-in List type.
    """

    list_id: UUID
    users: PyList[UUID]
    items: PyList[Item]
    sync_timestamp: datetime

    @field_validator("users")
    @classmethod
    def validate_users(cls, value: PyList[UUID]) -> PyList[UUID]:
        if not value:
            raise ValueError("A ShoppingList must have at least one user.")
        return value
