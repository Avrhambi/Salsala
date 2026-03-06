from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from shared.types import GeoCoordinates


class User(BaseModel):
    """
    Application user. user_id is a non-guessable UUID token fully decoupled
    from price data to preserve anonymized crowdsourcing integrity.
    """

    user_id: UUID
    display_name: str
    last_known_location: Optional[GeoCoordinates] = None

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("display_name must not be empty.")
        return value.strip()
