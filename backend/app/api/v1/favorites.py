from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.db.models.favorite import Favorite
from app.db.models.attraction import Attraction
from app.db.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteResponse, FavoriteList
from app.core.dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=FavoriteList)
async def get_favorites(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить список избранных достопримечательностей текущего пользователя"""
    result = await db.execute(
        select(Favorite)
        .options(selectinload(Favorite.attraction))
        .where(Favorite.user_id == current_user.id)
        .order_by(Favorite.created_at.desc())
    )
    favorites = result.scalars().all()

    return FavoriteList(
        items=[FavoriteResponse.model_validate(fav) for fav in favorites],
        total=len(favorites)
    )


@router.post("", response_model=FavoriteResponse, status_code=201)
async def add_to_favorites(
    favorite_data: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Добавить достопримечательность в избранное"""
    # Проверить существование достопримечательности
    attraction_result = await db.execute(
        select(Attraction).where(
            Attraction.id == favorite_data.attraction_id,
            Attraction.is_active == True
        )
    )
    attraction = attraction_result.scalar_one_or_none()

    if not attraction:
        raise HTTPException(status_code=404, detail="Attraction not found")

    # Проверить, не добавлена ли уже в избранное
    existing_result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.attraction_id == favorite_data.attraction_id
        )
    )
    existing = existing_result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Already in favorites")

    # Создать запись в избранном
    favorite = Favorite(
        user_id=current_user.id,
        attraction_id=favorite_data.attraction_id
    )
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)

    # Загрузить связанную достопримечательность
    result = await db.execute(
        select(Favorite)
        .options(selectinload(Favorite.attraction))
        .where(Favorite.id == favorite.id)
    )
    favorite_with_attraction = result.scalar_one()

    return FavoriteResponse.model_validate(favorite_with_attraction)


@router.delete("/{attraction_id}", status_code=204)
async def remove_from_favorites(
    attraction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удалить достопримечательность из избранного"""
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.attraction_id == attraction_id
        )
    )
    favorite = result.scalar_one_or_none()

    if not favorite:
        raise HTTPException(status_code=404, detail="Not in favorites")

    await db.delete(favorite)
    await db.commit()

    return None
