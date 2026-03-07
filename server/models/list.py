from datetime import datetime
from typing import List as PyList, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from server.models.item import Item


class ShoppingList(BaseModel):
    """
    A shopping list owned by one or more users.
    Named ShoppingList to avoid shadowing Python's built-in List type.
    """

    list_id: UUID
    name: str
    users: PyList[UUID]
    items: PyList[Item]
    is_completed: bool = False
    completed_at: Optional[datetime] = None

    @field_validator("users")
    @classmethod
    def validate_users(cls, value: PyList[UUID]) -> PyList[UUID]:
        if not value:
            raise ValueError("A ShoppingList must have at least one user.")
        return value
