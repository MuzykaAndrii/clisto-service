from typing import Any

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    Field,
    field_validator,
)


class ServiceOptionAdminSchema(BaseModel):
    name: str = Field(max_length=50, min_length=4)
    description: str | None = None
    video_url: AnyHttpUrl | str = ""
    subcategory: Any
    icon: Any

    @field_validator("video_url", mode="before")
    @classmethod
    def video_url_empty_to_none(cls, value) -> str | None:  # type: ignore
        if value == "":
            return None
        return value


class SubCategoryAdminSchema(BaseModel):
    name: str = Field(max_length=50, min_length=4)
    service_options: list[Any] | None = None
    category: Any


class CategoryAdminSchema(BaseModel):
    name: str = Field(max_length=50, min_length=4)
    subcategories: list[Any] | None = None
