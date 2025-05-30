from aiogram import Router, F
from aiogram.types import Message
from ..keyboards.user_keyboards import main_menu_kb

router = Router()


@router.message(F.text == "Категории товаров")
async def show_categories(message: Message):

    await message.answer("📂 Выберите категорию:", reply_markup=main_menu_kb())
