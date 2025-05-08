from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.db.database import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)

    products = relationship("ProductModel", back_populates="category")
