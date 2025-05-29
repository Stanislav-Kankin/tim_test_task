from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


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
