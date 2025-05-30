from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cart_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Оформить заказ", callback_data="checkout")
    builder.button(text="Очистить корзину", callback_data="clear_cart")
    builder.adjust(1)
    return builder.as_markup()


def back_to_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="В главное меню", callback_data="to_main")
    return builder.as_markup()


def main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text="Категории товаров")
    builder.button(text="Корзина")
    builder.button(text="Мои заказы")
    builder.button(text="Помощь")

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def categories_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text="Электроника")
    builder.button(text="Одежда")
    builder.button(text="Книги")
    builder.button(text="Главное меню")

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def generate_cart_keyboard(cart_items):
    buttons = [
        [InlineKeyboardButton(
            text=f"✏️ Изменить {item.product_name}",
            callback_data=f"edit_{item.id}"
            )]
        for item in cart_items
    ]
    buttons.append([InlineKeyboardButton(
        text="🧹 Очистить",
        callback_data="clear_cart")])
    buttons.append([InlineKeyboardButton(
        text="✅ Оформить",
        callback_data="checkout")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
