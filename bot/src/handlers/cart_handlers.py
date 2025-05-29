from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..models import get_db
from ..models.order import Cart
from ..keyboards.user_keyboards import cart_kb, back_to_menu_kb


import logging

router = Router()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.message(F.text == "Корзина")
async def show_cart(message: Message):
    try:
        async with get_db() as session:
            cart_items = await Cart.get_user_cart(session, message.from_user.id)

            if not cart_items:
                await message.answer(
                    "Ваша корзина пуста",
                    reply_markup=back_to_menu_kb()
                    )
                return

            total = sum(item.price * item.quantity for item in cart_items)
            items_text = "\n".join(
                f"{item.product_name} - {item.quantity} x {item.price} руб."
                for item in cart_items
            )

            await message.answer(
                f"Ваша корзина:\n\n{items_text}\n\nИтого: {total} руб.",
                reply_markup=cart_kb()
            )
    except Exception as e:
        await message.answer(
            "Произошла ошибка при загрузке корзины. Попробуйте позже.")

        logging.error(f"[!][!][!]Ошибка в show_cart: {e}")


@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery):
    try:
        async with get_db() as session:
            await Cart.clear_user_cart(session, callback.from_user.id)
            await callback.message.edit_text(
                "Корзина очищена",
                reply_markup=back_to_menu_kb()
            )
    except Exception as e:
        await callback.answer("Ошибка при очистке корзины")
        logging.error(f"[!][!][!]Ошибка в clear_cart: {e}")


@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):
    try:
        async with get_db() as session:
            cart_items = await Cart.get_user_cart(session, callback.from_user.id)

            if not cart_items:
                await callback.answer("Корзина пуста")
                return

            await callback.message.answer(
                "Пожалуйста, введите ваши данные для доставки в формате:\n"
                "ФИО, адрес, телефон"
            )
            await state.set_state("waiting_for_delivery_info")
    except Exception as e:
        await callback.answer("Ошибка при оформлении заказа")
        logging.error(f"[!][!][!]Ошибка в checkout: {e}")


@router.message(state="waiting_for_delivery_info")
async def process_delivery_info(message: Message, state: FSMContext):
    try:
        delivery_info = message.text
        async with get_db() as session:
            # Создаем заказ из корзины
            order_id = await Order.create_from_cart(
                session,
                message.from_user.id,
                delivery_info
                )

            await message.answer(
                f"Заказ #{order_id} оформлен!\n"
                "Наш менеджер свяжется с вами для подтверждения.",
                reply_markup=main_menu_kb()
            )
            await state.clear()
    except Exception as e:
        await message.answer("Ошибка при обработке заказа")
        logging.error(f"Error in process_delivery_info: {e}")
