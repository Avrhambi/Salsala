from uuid import UUID

from pydantic import BaseModel, field_validator


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
        if value < 0:
            raise ValueError(
                f"data_points must be non-negative, received {value}."
            )
        return value
