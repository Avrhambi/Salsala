from uuid import UUID

from pydantic import BaseModel, field_validator

from shared.types import GeoCoordinates

MINIMUM_CHAIN_LENGTH = 1


class Store(BaseModel):
    """
    A physical retail store location with geographic coordinates.
    Chain identifies the parent supermarket brand (e.g. "Shufersal").
    """

    store_id: UUID
    name: str
    coordinates: GeoCoordinates
    chain: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Store name must not be empty.")
        return value.strip()

    @field_validator("chain")
    @classmethod
    def validate_chain(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Store chain must not be empty.")
        return value.strip()
