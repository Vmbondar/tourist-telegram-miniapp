"""
Скрипт для заполнения базы данных тестовыми данными
"""
import asyncio
import sys
from pathlib import Path

# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import City, Attraction


async def create_test_data():
    """Создание тестовых данных для MVP"""
    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже данные
        result = await session.execute(select(City))
        existing_cities = result.scalars().all()

        if existing_cities:
            print("⚠️  База данных уже содержит данные. Пропускаем...")
            return

        print("📝 Создание тестовых данных...")

        # Создаем города
        moscow = City(
            name="Москва",
            country="Россия"
        )
        spb = City(
            name="Санкт-Петербург",
            country="Россия"
        )

        session.add_all([moscow, spb])
        await session.flush()  # Получаем ID городов

        print(f"✅ Созданы города: {moscow.name}, {spb.name}")

        # Достопримечательности Москвы
        moscow_attractions = [
            Attraction(
                city_id=moscow.id,
                name="Красная площадь",
                description="Главная площадь Москвы, расположенная в центре города. Объект Всемирного наследия ЮНЕСКО.",
                address="Красная площадь, Москва",
                photo_url="https://images.unsplash.com/photo-1513326738677-b964603b136d",
                category="Площадь",
                rating=4.8
            ),
            Attraction(
                city_id=moscow.id,
                name="Храм Василия Блаженного",
                description="Православный храм на Красной площади, один из самых узнаваемых символов России.",
                address="Красная площадь, 7, Москва",
                photo_url="https://images.unsplash.com/photo-1512495039889-d18c6f0d6706",
                category="Храм",
                rating=4.9
            ),
            Attraction(
                city_id=moscow.id,
                name="Московский Кремль",
                description="Древнейшая часть Москвы, резиденция Президента РФ. Музей-заповедник.",
                address="Кремль, Москва",
                photo_url="https://images.unsplash.com/photo-1547448415-e9f5b28e570d",
                category="Крепость",
                rating=4.7
            ),
            Attraction(
                city_id=moscow.id,
                name="Третьяковская галерея",
                description="Крупнейший музей русского искусства в мире.",
                address="Лаврушинский переулок, 10, Москва",
                photo_url="https://images.unsplash.com/photo-1595433707802-6b2626ef1c91",
                category="Музей",
                rating=4.8
            ),
            Attraction(
                city_id=moscow.id,
                name="Парк Горького",
                description="Центральный парк культуры и отдыха имени Максима Горького.",
                address="Крымский Вал, 9, Москва",
                photo_url="https://images.unsplash.com/photo-1625398407796-82650a8c135f",
                category="Парк",
                rating=4.6
            ),
            Attraction(
                city_id=moscow.id,
                name="Большой театр",
                description="Один из крупнейших в мире театров оперы и балета.",
                address="Театральная площадь, 1, Москва",
                photo_url="https://images.unsplash.com/photo-1590247813693-5541d1c609fd",
                category="Театр",
                rating=4.9
            ),
            Attraction(
                city_id=moscow.id,
                name="Воробьевы горы",
                description="Природный заказник с панорамным видом на Москву.",
                address="Воробьевы горы, Москва",
                photo_url="https://images.unsplash.com/photo-1556114220-3f17cdfbe3e0",
                category="Смотровая площадка",
                rating=4.7
            ),
        ]

        # Достопримечательности Санкт-Петербурга
        spb_attractions = [
            Attraction(
                city_id=spb.id,
                name="Эрмитаж",
                description="Один из крупнейших и значимых художественных и культурно-исторических музеев мира.",
                address="Дворцовая площадь, 2, Санкт-Петербург",
                photo_url="https://images.unsplash.com/photo-1583422409516-2895a77efded",
                category="Музей",
                rating=4.9
            ),
            Attraction(
                city_id=spb.id,
                name="Петергоф",
                description="Дворцово-парковый ансамбль, известный своими фонтанами.",
                address="Разводная ул., 2, Петергоф",
                photo_url="https://images.unsplash.com/photo-1564585497019-34d341e13054",
                category="Дворец",
                rating=4.8
            ),
            Attraction(
                city_id=spb.id,
                name="Храм Спаса на Крови",
                description="Православный храм в историческом центре Санкт-Петербурга.",
                address="Набережная канала Грибоедова, 2Б, Санкт-Петербург",
                photo_url="https://images.unsplash.com/photo-1581196831125-93df9dca8b68",
                category="Храм",
                rating=4.9
            ),
            Attraction(
                city_id=spb.id,
                name="Дворцовая площадь",
                description="Главная площадь Санкт-Петербурга, объект Всемирного наследия ЮНЕСКО.",
                address="Дворцовая площадь, Санкт-Петербург",
                photo_url="https://images.unsplash.com/photo-1621524475924-ade39a0ebdd6",
                category="Площадь",
                rating=4.8
            ),
            Attraction(
                city_id=spb.id,
                name="Невский проспект",
                description="Главная улица Санкт-Петербурга.",
                address="Невский проспект, Санкт-Петербург",
                photo_url="https://images.unsplash.com/photo-1609356765656-a3d5e2c6c5d5",
                category="Улица",
                rating=4.7
            ),
            Attraction(
                city_id=spb.id,
                name="Петропавловская крепость",
                description="Историческое ядро Санкт-Петербурга, крепость на Заячьем острове.",
                address="Петропавловская крепость, 3, Санкт-Петербург",
                photo_url="https://images.unsplash.com/photo-1587471364504-efe1ab5a966c",
                category="Крепость",
                rating=4.7
            ),
            Attraction(
                city_id=spb.id,
                name="Исаакиевский собор",
                description="Крупнейший православный храм Санкт-Петербурга.",
                address="Исаакиевская площадь, 4, Санкт-Петербург",
                photo_url="https://images.unsplash.com/photo-1562699619-79e5dac78d99",
                category="Храм",
                rating=4.8
            ),
        ]

        session.add_all(moscow_attractions + spb_attractions)
        await session.commit()

        print(f"✅ Создано {len(moscow_attractions)} достопримечательностей для Москвы")
        print(f"✅ Создано {len(spb_attractions)} достопримечательностей для Санкт-Петербурга")
        print("\n🎉 Тестовые данные успешно созданы!")


async def main():
    """Основная функция"""
    try:
        await create_test_data()
    except Exception as e:
        print(f"❌ Ошибка при создании тестовых данных: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
