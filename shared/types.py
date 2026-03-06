from enum import Enum

from pydantic import BaseModel, field_validator


class TrendValue(str, Enum):
    """Directional price trend used by the Price Intelligence Engine."""

    UP = "UP"
    DOWN = "DOWN"
    STABLE = "STABLE"
    NA = "N/A"


class GeoCoordinates(BaseModel):
    """Geographic coordinate pair used by the Geographic Value Optimizer."""

    latitude: float
    longitude: float

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: float) -> float:
        if not (-90.0 <= value <= 90.0):
            raise ValueError(
                f"latitude must be between -90 and 90, received {value}."
            )
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: float) -> float:
        if not (-180.0 <= value <= 180.0):
            raise ValueError(
                f"longitude must be between -180 and 180, received {value}."
            )
        return value
