from starlette_admin.contrib.sqla.ext.pydantic import ModelView

from app.modules.auto_maintenance.admin.schemas import (
    CategoryAdminSchema,
    ServiceOptionAdminSchema,
    SubCategoryAdminSchema,
)
from app.modules.auto_maintenance.models import (
    Category,
    ServiceOption,
    Subcategory,
)


class CategoryAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = Category
        pydantic_model = CategoryAdminSchema
        icon = "fa-regular fa-folder"
        name = "Category"
        label = "Categories"

        super().__init__(model, pydantic_model, icon, name, label)

    fields = [
        Category.id,
        Category.name,
        Category.subcategories,
    ]


class SubCategoryAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = Subcategory
        pydantic_model = SubCategoryAdminSchema
        icon = "fa-regular fa-folder-open"
        name = "Subcategory"
        label = "Subcategories"

        super().__init__(model, pydantic_model, icon, name, label)

    fields = [
        Subcategory.id,
        Subcategory.name,
        Subcategory.category,
        Subcategory.service_options,
    ]


class ServiceOptionAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = ServiceOption
        pydantic_model = ServiceOptionAdminSchema
        icon = "fa-solid fa-wrench"
        name = "Service"
        label = "Services"

        super().__init__(model, pydantic_model, icon, name, label)

    fields = [
        ServiceOption.id,
        ServiceOption.name,
        ServiceOption.description,
        ServiceOption.video_url,
        ServiceOption.subcategory,
        ServiceOption.icon,
    ]

    exclude_fields_from_list = [ServiceOption.description]

    edit_template = "custom_edit.html"
    list_template = "custom_list.html"
    detail_template = "custom_detail.html"
