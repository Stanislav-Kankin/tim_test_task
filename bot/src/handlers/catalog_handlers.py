from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
import logging
from pathlib import Path

from models import Category, Subcategory, Product, Cart
from models import get_db
from keyboards.user_keyboards import get_categories_kb, get_subcategories_kb

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == "Категории товаров")
async def show_categories(message: Message):
    async with get_db() as session:
        result = await session.execute(select(Category))
        categories = result.scalars().all()

    if categories:
        await message.answer("Выберите категорию:", reply_markup=get_categories_kb(categories))
    else:
        await message.answer("Категорий пока нет")


@router.callback_query(F.data.startswith("category:"))
async def show_subcategories(callback: CallbackQuery):
    category_id = int(callback.data.split(":")[1])
    async with get_db() as session:
        result = await session.execute(select(Subcategory).where(Subcategory.category_id == category_id))
        subcategories = result.scalars().all()

    if subcategories:
        await callback.message.edit_text("Выберите подкатегорию:", reply_markup=get_subcategories_kb(subcategories))
    else:
        await callback.message.edit_text("Подкатегорий пока нет.")


@router.callback_query(F.data.startswith("subcategory:"))
async def show_products(callback: CallbackQuery):
    subcategory_id = int(callback.data.split(":")[1])
    async with get_db() as session:
        result = await session.execute(select(Product).where(Product.subcategory_id == subcategory_id))
        products = result.scalars().all()

    if not products:
        await callback.message.edit_text("Товаров пока нет.")
        return

    for product in products:
        text = (
            f"<b>{product.name}</b>\n\n"
            f"{product.description}\n\n"
            f"<b>Цена: {product.price} руб.</b>"
        )
        builder = InlineKeyboardBuilder()
        builder.button(text="В корзину", callback_data=f"add:{product.id}")
        builder.adjust(1)

        photo_path = f"/app/img/{product.photo_url}"

        try:
            photo = FSInputFile(photo_path)
        except Exception as e:
            logger.error(f"Ошибка при загрузке фото: {e}")
            photo = None

        if photo:
            await callback.message.answer_photo(
                photo=photo,
                caption=text,
                reply_markup=builder.as_markup()
            )
        else:
            await callback.message.answer(
                text=text,
                reply_markup=builder.as_markup()
            )


@router.callback_query(F.data.startswith("add:"))
async def add_product_to_cart(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[1])
    try:
        async with get_db() as session:
            product = await session.get(Product, product_id)
            if not product:
                await callback.answer("Товар не найден")
                return
            await Cart.add_to_cart(session, callback.from_user.id, product.name, 1, float(product.price))
            await callback.answer(f"{product.name} добавлен в корзину!")
    except Exception as e:
        await callback.answer("Ошибка при добавлении")
        logger.error(f"[add_product_to_cart] Ошибка: {e}")


@router.message(F.text == "/test")
async def test_inline_button(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Нажми меня", callback_data="test_click")
    await message.answer("Вот кнопка:", reply_markup=builder.as_markup())


@router.callback_query(F.data == "test_click")
async def test_click_handler(callback: CallbackQuery):
    await callback.answer("Кнопка работает!")
