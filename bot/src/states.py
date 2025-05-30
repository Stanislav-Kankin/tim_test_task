from aiogram.fsm.state import StatesGroup, State


class CheckoutState(StatesGroup):
    waiting_for_delivery_info = State()


class CatalogStates(StatesGroup):
    categories = State()
    subcategories = State()
