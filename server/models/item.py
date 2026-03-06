from uuid import UUID

from pydantic import BaseModel, field_validator


class Item(BaseModel):
    """A grocery item that appears on a Salsala shopping list."""

    id: UUID
    name_hebrew: str
    default_quantity: int

    @field_validator("name_hebrew")
    @classmethod
    def validate_name_hebrew(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("name_hebrew must not be empty or whitespace-only.")
        return value.strip()

    @field_validator("default_quantity")
    @classmethod
    def validate_default_quantity(cls, value: int) -> int:
        if value < 0:
            raise ValueError(
                f"default_quantity must be non-negative, received {value}."
            )
        return value
