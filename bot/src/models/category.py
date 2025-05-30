from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.db import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    subcategories = relationship("Subcategory", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
