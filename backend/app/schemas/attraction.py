from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class AttractionBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    photo_url: Optional[str] = None
    category: Optional[str] = None


class AttractionCreate(AttractionBase):
    city_id: int


class AttractionResponse(AttractionBase):
    id: int
    city_id: int
    rating: float
    is_active: bool
    created_at: datetime
    is_favorite: Optional[bool] = False  # Будет заполняться в API

    model_config = ConfigDict(from_attributes=True)


class AttractionList(BaseModel):
    items: list[AttractionResponse]
    total: int
    page: int
    page_size: int
