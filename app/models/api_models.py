from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class Parcel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    status: str = Field(min_length=1)
    category: str = Field(min_length=1)
    created: date = Field(strict=False)


class ParcelPage(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    items: list[Parcel]
    offset: int = Field(ge=0)
    limit: int = Field(gt=0)
    total: int = Field(ge=0)
