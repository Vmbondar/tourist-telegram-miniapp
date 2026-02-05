from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.session import init_db, close_db
from app.api.v1 import auth_router
from app.api.v1.cities import router as cities_router
from app.api.v1.attractions import router as attractions_router
from app.api.v1.favorites import router as favorites_router


async def seed_database():
    """Заполнение БД тестовыми данными при первом запуске"""
    from sqlalchemy import select
    from app.db.session import AsyncSessionLocal
    from app.db.models.city import City

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(City))
        if result.scalars().first():
            return

    # Импортируем и запускаем seed только если БД пуста
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.seed_data import create_test_data
    await create_test_data()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup
    await init_db()
    await seed_database()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(cities_router, prefix="/api/v1/cities", tags=["cities"])
app.include_router(attractions_router, prefix="/api/v1/attractions", tags=["attractions"])
app.include_router(favorites_router, prefix="/api/v1/favorites", tags=["favorites"])


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Welcome to Tourist Telegram Mini App API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "healthy"}
