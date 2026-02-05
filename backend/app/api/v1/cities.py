from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models.city import City
from app.schemas.city import CityResponse, CityList

router = APIRouter()


@router.get("", response_model=CityList)
async def get_cities(
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех активных городов"""
    result = await db.execute(
        select(City).where(City.is_active == True).order_by(City.name)
    )
    cities = result.scalars().all()

    return CityList(
        items=[CityResponse.model_validate(city) for city in cities],
        total=len(cities)
    )


@router.get("/{city_id}", response_model=CityResponse)
async def get_city(
    city_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о конкретном городе"""
    result = await db.execute(
        select(City).where(City.id == city_id, City.is_active == True)
    )
    city = result.scalar_one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return CityResponse.model_validate(city)
