from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.db.session import get_db
from app.db.models.attraction import Attraction
from app.db.models.favorite import Favorite
from app.db.models.user import User
from app.schemas.attraction import AttractionResponse, AttractionList
from app.core.dependencies import get_current_user_optional

router = APIRouter()


async def check_is_favorite(
    attraction_ids: list[int],
    user_id: Optional[int],
    db: AsyncSession
) -> set[int]:
    """Проверить, какие достопримечательности в избранном у пользователя"""
    if not user_id:
        return set()

    result = await db.execute(
        select(Favorite.attraction_id).where(
            Favorite.user_id == user_id,
            Favorite.attraction_id.in_(attraction_ids)
        )
    )
    return set(result.scalars().all())


@router.get("", response_model=AttractionList)
async def get_attractions(
    city_id: Optional[int] = Query(None, description="Фильтр по городу"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Получить список достопримечательностей с фильтрацией и пагинацией"""
    query = select(Attraction).where(Attraction.is_active == True)

    if city_id:
        query = query.where(Attraction.city_id == city_id)

    if category:
        query = query.where(Attraction.category == category)

    # Получить общее количество
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Применить пагинацию
    query = query.order_by(Attraction.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    attractions = result.scalars().all()

    # Проверить избранное
    attraction_ids = [a.id for a in attractions]
    favorite_ids = await check_is_favorite(
        attraction_ids,
        current_user.id if current_user else None,
        db
    )

    # Добавить флаг is_favorite
    items = []
    for attraction in attractions:
        attraction_dict = AttractionResponse.model_validate(attraction).model_dump()
        attraction_dict['is_favorite'] = attraction.id in favorite_ids
        items.append(AttractionResponse(**attraction_dict))

    return AttractionList(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{attraction_id}", response_model=AttractionResponse)
async def get_attraction(
    attraction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Получить детальную информацию о достопримечательности"""
    result = await db.execute(
        select(Attraction).where(
            Attraction.id == attraction_id,
            Attraction.is_active == True
        )
    )
    attraction = result.scalar_one_or_none()

    if not attraction:
        raise HTTPException(status_code=404, detail="Attraction not found")

    # Проверить избранное
    favorite_ids = await check_is_favorite(
        [attraction_id],
        current_user.id if current_user else None,
        db
    )

    attraction_dict = AttractionResponse.model_validate(attraction).model_dump()
    attraction_dict['is_favorite'] = attraction_id in favorite_ids

    return AttractionResponse(**attraction_dict)
