from typing import Annotated, List
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from server.models.transaction import Transaction

CONFIDENCE_SCORE_MIN = 0.0
CONFIDENCE_SCORE_MAX = 1.0


class Receipt(BaseModel):
    """An OCR-processed receipt linked to one or more parsed transactions."""

    receipt_id: UUID
    image_url: str
    confidence_score: Annotated[
        float,
        Field(
            ge=CONFIDENCE_SCORE_MIN,
            le=CONFIDENCE_SCORE_MAX,
            description="OCR confidence between 0.0 and 1.0.",
        ),
    ]
    requires_human_verification: bool
    parsed_items: List[Transaction]

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("image_url must not be empty.")
        return value.strip()
