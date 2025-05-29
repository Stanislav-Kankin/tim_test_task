import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from models import Base

DATABASE_URL = (
    "postgresql+asyncpg://stanislav:12345@db:5432/db_shop"
)


async def init_db():
    engine = create_async_engine(DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Таблицы успешно созданы!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
