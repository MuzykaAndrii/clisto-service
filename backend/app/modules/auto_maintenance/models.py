from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "maintenance_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)

    subcategories = relationship("Subcategory", back_populates="category")


class Subcategory(Base):
    __tablename__ = "maintenance_subcategories"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    category_id = Column(ForeignKey("maintenance_categories.id"), nullable=False)

    category = relationship("Category", back_populates="subcategories")
    service_options = relationship("ServiceOptions", back_populates="subcategory")


class ServiceOption(Base):
    __tablename__ = "maintenance_services"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    subcategory_id = Column(ForeignKey("maintenance_subcategories.id"), nullable=False)
    # TODO: add field to store icon

    subcategory = relationship("Subcategory", back_populates="service_options")
