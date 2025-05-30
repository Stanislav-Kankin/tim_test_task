from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from src.database.models import Category, Subcategory, Product
from src.database.session import async_session
from src.keyboards.user_keyboards import get_categories_kb, get_subcategories_kb

router = Router()


@router.message(F.text == "Категории товаров")
async def show_categories(message: Message):
    async with async_session() as session:
        result = await session.execute(select(Category))
        categories = result.scalars().all()

    if categories:
        await message.answer("📂 Выберите категорию:", reply_markup=get_categories_kb(categories))
    else:
        await message.answer("Категорий пока нет 😕")


@router.callback_query(F.data.startswith("category:"))
async def show_subcategories(callback: CallbackQuery):
    category_id = int(callback.data.split(":")[1])
    async with async_session() as session:
        result = await session.execute(
            select(Subcategory).where(Subcategory.category_id == category_id)
        )
        subcategories = result.scalars().all()

    if subcategories:
        await callback.message.edit_text(
            "📁 Выберите подкатегорию:",
            reply_markup=get_subcategories_kb(subcategories)
        )
    else:
        await callback.message.edit_text("Подкатегорий пока нет.")


@router.callback_query(F.data.startswith("subcategory:"))
async def show_products(callback: CallbackQuery):
    subcategory_id = int(callback.data.split(":")[1])
    async with async_session() as session:
        result = await session.execute(
            select(Product).where(Product.subcategory_id == subcategory_id)
        )
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
        await callback.message.answer_photo(
            photo=product.photo_url,
            caption=text,
            reply_markup=None  # Можно позже сделать кнопку "Добавить в корзину"
        )


@router.message(F.text == "/test")
async def test_inline_button(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Нажми меня", callback_data="test_click")]
        ]
    )
    await message.answer("Вот кнопка:", reply_markup=keyboard)


@router.callback_query(F.data == "test_click")
async def test_click_handler(callback: CallbackQuery):
    await callback.answer("Кнопка работает!")
