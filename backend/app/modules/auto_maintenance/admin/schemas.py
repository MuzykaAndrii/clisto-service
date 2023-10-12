from typing import Any

from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
    field_validator,
)


class ServiceOptionAdminSchema(BaseModel):
    name: str = Field(max_length=50, min_length=4)
    description: str | None = None
    video_url: AnyUrl = None
    subcategory: Any
    icon: Any


class SubCategoryAdminSchema(BaseModel):
    name: str = Field(max_length=50, min_length=4)
    service_options: list[Any] = None
    category: Any


class CategoryAdminSchema(BaseModel):
    name: str = Field(max_length=50, min_length=4)
    subcategories: list[Any] = None
