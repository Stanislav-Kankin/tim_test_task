import asyncio
from src.models import Base, engine
from sqlalchemy.engine.url import make_url


async def init_db():
    print(f"📦 Подключаюсь к базе: {make_url(engine.url)}")

    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Таблицы успешно созданы!")
        except Exception as e:
            print(f"❌ Ошибка при создании таблиц: {e}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
