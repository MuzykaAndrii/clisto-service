from app.schemas import BaseSchema


class ServiceOptionSchema(BaseSchema):
    name: str


class SubcategorySchema(BaseSchema):
    name: str
    service_options: list[ServiceOptionSchema]


class CategorySchema(BaseSchema):
    name: str
    subcategories: list[SubcategorySchema]
