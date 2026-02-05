from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.attraction import AttractionResponse


class FavoriteCreate(BaseModel):
    attraction_id: int


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    attraction_id: int
    created_at: datetime
    attraction: AttractionResponse

    model_config = ConfigDict(from_attributes=True)


class FavoriteList(BaseModel):
    items: list[FavoriteResponse]
    total: int
