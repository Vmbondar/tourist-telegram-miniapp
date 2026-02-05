from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    country: Optional[str] = "Russia"


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CityList(BaseModel):
    items: list[CityResponse]
    total: int
