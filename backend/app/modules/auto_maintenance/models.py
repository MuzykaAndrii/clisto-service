from fastapi import Request
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy_file import ImageField
from sqlalchemy_file.validators import ImageValidator

from app.db.base import Base


class Category(Base):
    __tablename__ = "maintenance_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)

    subcategories = relationship(
        "Subcategory", back_populates="category", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"Category: {self.name}"

    def __repr__(self) -> str:
        return str(self)

    def __admin_repr__(self, request: Request) -> str:
        return str(self)


class Subcategory(Base):
    __tablename__ = "maintenance_subcategories"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    category_id = Column(ForeignKey("maintenance_categories.id"), nullable=False)

    category = relationship("Category", back_populates="subcategories")
    service_options = relationship("ServiceOption", back_populates="subcategory")

    def __str__(self) -> str:
        return f"Subcategory: {self.name}"

    def __repr__(self) -> str:
        return str(self)

    def __admin_repr__(self, request: Request) -> str:
        return str(self)


class ServiceOption(Base):
    __tablename__ = "maintenance_services"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    subcategory_id = Column(ForeignKey("maintenance_subcategories.id"), nullable=False)
    icon = Column(
        ImageField(
            image_validator=ImageValidator(
                allowed_content_types=["image/svg+xml", "image/png"]
            ),
            upload_storage="services-icons",
        )
    )

    subcategory = relationship(Subcategory, back_populates="service_options")

    def __str__(self) -> str:
        return f"Service option: {self.name}"

    def __repr__(self) -> str:
        return str(self)

    def __admin_repr__(self, request: Request) -> str:
        return f"Service: {self.name}"
