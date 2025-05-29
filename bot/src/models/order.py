from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .user import Base
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_name = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)

    @classmethod
    async def get_user_cart(cls, session: AsyncSession, user_id: int):
        result = await session.execute(select(cls).where(
            cls.user_id == user_id
            ))
        return result.scalars().all()

    @classmethod
    async def clear_user_cart(cls, session: AsyncSession, user_id: int):
        await session.execute(delete(cls).where(cls.user_id == user_id))
        await session.commit()


class Order(Base):
    # ... предыдущий код ...

    @classmethod
    async def create_from_cart(cls, session: AsyncSession, user_id: int, delivery_info: str) -> int:
        cart_items = await Cart.get_user_cart(session, user_id)

        if not cart_items:
            raise ValueError("Корзина пуста!")

        # Создаем заказ для каждого товара
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

        # Очищаем корзину
        await Cart.clear_user_cart(session, user_id)

        await session.commit()
        return order.id  # Возвращаем ID последнего заказа
