from aiogram import types, Bot
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User
import logging


class SubscriptionCheckMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot = bot
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Пропускаем проверку для команд start и help
        if isinstance(event, types.Message) and event.text in ["/start", "/help"]:
            return await handler(event, data)

        session: AsyncSession = data["session"]
        user = event.from_user

        try:
            db_user = await User.get_user_by_telegram_id(session, user.id)
            if not db_user or not db_user.is_subscribed:
                await event.answer(
                    "Для использования бота необходимо подписаться на нашу группу.\n"
                    "Пожалуйста, подпишитесь и попробуйте снова."
                )
                return

            return await handler(event, data)
        except Exception as e:
            logging.error(f"Subscription check error: {e}")
            await event.answer(
                "Произошла ошибка при проверке подписки. Попробуйте позже."
                )
            return
