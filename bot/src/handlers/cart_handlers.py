from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from ..states import CheckoutState
from ..models.order import Order, Cart
from ..models import get_db
from ..keyboards.user_keyboards import cart_kb, back_to_menu_kb, main_menu_kb

import logging

router = Router()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.message(F.text.startswith("/add"))
async def add_to_cart(message: Message):
    try:
        parts = message.text.replace("/add", "").strip().split(",")

        if len(parts) != 3:
            await message.answer("Формат: /add Название, Кол-во, Цена")
            return

        product_name = parts[0].strip()
        quantity = int(parts[1])
        price = float(parts[2])

        async with get_db() as session:
            await Cart.add_to_cart(
                session, message.from_user.id, product_name, quantity, price
            )

        await message.answer(f"✅ Товар {product_name} добавлен в корзину!")

    except Exception as e:
        await message.answer("Ошибка при добавлении в корзину")
        logger.error(f"[add_to_cart] Ошибка: {e}")


@router.message(F.text == "Корзина")
async def show_cart(message: Message):
    try:
        async with get_db() as session:
            cart_items = await Cart.get_user_cart(session, message.from_user.id)

        if not cart_items:
            await message.answer("Ваша корзина пуста", reply_markup=back_to_menu_kb())
            return

        total = sum(item.price * item.quantity for item in cart_items)
        items_text = "\n".join(
            f"{item.product_name} - {item.quantity} x {item.price} руб."
            for item in cart_items
        )

        await message.answer(
            f"🛒 Ваша корзина:\n\n{items_text}\n\nИтого: {total} руб.",
            reply_markup=cart_kb()
        )
    except Exception as e:
        await message.answer("Ошибка при загрузке корзины")
        logger.error(f"[show_cart] Ошибка: {e}")


@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery):
    try:
        async with get_db() as session:
            await Cart.clear_user_cart(session, callback.from_user.id)

        await callback.message.edit_text("🧹 Корзина очищена", reply_markup=back_to_menu_kb())
    except Exception as e:
        await callback.answer("Ошибка при очистке корзины")
        logger.error(f"[clear_cart] Ошибка: {e}")


@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):
    try:
        async with get_db() as session:
            cart_items = await Cart.get_user_cart(session, callback.from_user.id)

        if not cart_items:
            await callback.answer("Корзина пуста")
            return

        await callback.message.answer(
            "📦 Введите данные для доставки в формате:\nФИО, адрес, телефон"
        )
        await state.set_state(CheckoutState.waiting_for_delivery_info)
    except Exception as e:
        await callback.answer("Ошибка при оформлении заказа")
        logger.error(f"[checkout] Ошибка: {e}")


@router.message(StateFilter(CheckoutState.waiting_for_delivery_info))
async def process_delivery_info(message: Message, state: FSMContext):
    try:
        delivery_info = message.text
        async with get_db() as session:
            order_id = await Order.create_from_cart(
                session,
                message.from_user.id,
                delivery_info
            )

        await message.answer(
            f"✅ Заказ #{order_id} оформлен!\nНаш менеджер свяжется с вами.",
            reply_markup=main_menu_kb()
        )
        await state.clear()
    except Exception as e:
        await message.answer("Ошибка при оформлении заказа")
        logger.error(f"[process_delivery_info] Ошибка: {e}")


@router.message(F.text == "Мои заказы")
async def my_orders(message: Message):
    try:
        async with get_db() as session:
            orders = await Order.get_user_orders(session, message.from_user.id)

        if not orders:
            await message.answer("У вас пока нет заказов.")
            return

        orders_text = "\n\n".join(
            f"📦 #{o.id} — {o.product_name} x{o.quantity}, {o.status}\n"
            f"📍 {o.delivery_info}" for o in orders
        )

        await message.answer(f"Ваши заказы:\n\n{orders_text}")
    except Exception as e:
        await message.answer("Ошибка при загрузке заказов")
        logger.error(f"[my_orders] Ошибка: {e}")


@router.message(F.text == "Помощь")
async def help_handler(message: Message):
    await message.answer(
        "📋 Команды:\n"
        "/start — начать\n"
        "/menu — главное меню\n"
        "/add Название, Кол-во, Цена — добавить товар"
    )
