from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    photo_url = Column(String(500))
    price = Column(Float, nullable=False)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))

    subcategory = relationship("Subcategory", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
