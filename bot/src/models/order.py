from sqlalchemy import (
    Column, Integer, String, Float,
    ForeignKey, select, delete
)
from sqlalchemy.ext.asyncio import AsyncSession
from . import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product_name = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)

    @classmethod
    async def get_user_cart(cls, session: AsyncSession, user_id: int):
        result = await session.execute(
            select(cls).where(cls.user_id == user_id)
        )
        return result.scalars().all()

    @classmethod
    async def add_to_cart(
        cls,
        session: AsyncSession,
        user_id: int,
        product_name: str,
        quantity: int,
        price: float
    ):
        cart_item = cls(
            user_id=user_id,
            product_name=product_name,
            quantity=quantity,
            price=price
        )
        session.add(cart_item)
        await session.commit()

    @classmethod
    async def clear_user_cart(cls, session: AsyncSession, user_id: int):
        await session.execute(delete(cls).where(cls.user_id == user_id))
        await session.commit()


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product_name = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)
    status = Column(String(50), default="processing")
    delivery_info = Column(String(500), nullable=True)

    @classmethod
    async def create_from_cart(
        cls,
        session: AsyncSession,
        user_id: int,
        delivery_info: str
    ) -> int:
        cart_items = await Cart.get_user_cart(session, user_id)
        if not cart_items:
            raise ValueError("Корзина пуста!")

        last_order_id = None
        for item in cart_items:
            order = cls(
                user_id=user_id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price,
                status="processing",
                delivery_info=delivery_info
            )
            session.add(order)
            last_order_id = order  # сохраним последний объект

        await Cart.clear_user_cart(session, user_id)
        await session.commit()
        return last_order_id.id if last_order_id else -1

    @classmethod
    async def get_user_orders(cls, session: AsyncSession, user_id: int):
        result = await session.execute(
            select(cls).where(cls.user_id == user_id)
        )
        return result.scalars().all()
