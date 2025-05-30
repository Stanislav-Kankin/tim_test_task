from sqlalchemy import Column, Integer, String
from .db import Base


class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Catalog(id={self.id}, title='{self.title}')>"
