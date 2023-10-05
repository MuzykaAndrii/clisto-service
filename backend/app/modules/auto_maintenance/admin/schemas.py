from typing import Any

from pydantic import (
    BaseModel,
    Field,
)


class ServiceOptionAdminSchema(BaseModel):
    name: str = Field(max_length=50, min_length=4)
    subcategory: Any
    icon: Any


class SubCategoryAdminSchema(BaseModel):
    name: str = Field(max_length=50, min_length=4)
    service_options: list[Any] = None
    category: Any


class CategoryAdminSchema(BaseModel):
    name: str = Field(max_length=50, min_length=4)
    subcategories: list[Any] = None
