import asyncio
import logging
from . import bot, dp

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    try:
        logger.info("[!] БОТ ЗАПУЩЕН [!]")

        # Очистка обновлений, если бот был перезапущен
        await bot.delete_webhook(drop_pending_updates=True)

        # Запуск поллинга
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Bot stopped with error: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
