from uuid import UUID

from pydantic import BaseModel, field_validator

MINIMUM_DATA_POINTS = 1


class Benchmark(BaseModel):
    """
    National price benchmark for a single item at a specific store,
    derived from crowdsourced transaction data.
    """

    item_id: UUID
    store_id: UUID
    national_avg: float
    data_points: int

    @field_validator("national_avg")
    @classmethod
    def validate_national_avg(cls, value: float) -> float:
        if value < 0:
            raise ValueError(
                f"national_avg must be non-negative, received {value}."
            )
        return value

    @field_validator("data_points")
    @classmethod
    def validate_data_points(cls, value: int) -> int:
        if value < MINIMUM_DATA_POINTS:
            raise ValueError(
                f"data_points must be at least {MINIMUM_DATA_POINTS}, received {value}."
            )
        return value
