from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import logging

from ..keyboards.user_keyboards import main_menu_kb

router = Router()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message):
    try:
        await message.answer(
            "Добро пожаловать в бота!\n\n"
            "Пожалуйста, подпишитесь на нашу группу, чтобы продолжить.",
            reply_markup=main_menu_kb()
        )
    except Exception as e:
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")
        logging.error(f"[!][!][!]Ошибка в cmd_start: {e}")


@router.message(Command("help"))
async def cmd_help(message: Message):
    try:
        await message.answer(
            "Список доступных команд:\n"
            "/start - Начать работу с ботом\n"
            "/help - Получить справку\n"
            "/menu - Открыть главное меню"
        )
    except Exception as e:
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")
        logging.error(f"[!][!][!]Ошибка в cmd_help: {e}")


@router.message(F.text == "Главное меню")
@router.message(Command("menu"))
async def main_menu(message: Message):
    try:
        await message.answer(
            "Выберите действие:",
            reply_markup=main_menu_kb()
        )
    except Exception as e:
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")
        logging.error(f"[!][!][!]Ошибка в main_menu: {e}")
