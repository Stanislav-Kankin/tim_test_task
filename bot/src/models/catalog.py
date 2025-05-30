from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from . import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    subcategories = relationship(
        "Subcategory",
        back_populates="category",
        cascade="all, delete"
        )


class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="subcategories")
    products = relationship(
        "Product",
        back_populates="subcategory",
        cascade="all, delete"
        )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String(255), nullable=True)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))

    subcategory = relationship("Subcategory", back_populates="products")
