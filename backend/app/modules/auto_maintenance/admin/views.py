from starlette_admin.contrib.sqla import ModelView

from app.modules.auto_maintenance.models import (
    Category,
    ServiceOption,
    Subcategory,
)


class CategoryAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = Category
        icon = "fa-regular fa-folder"
        name = "Category"
        label = "Categories"
        identity = None
        converter = None

        super().__init__(model, icon, name, label, identity, converter)

    fields = [
        Category.id,
        Category.name,
        Category.subcategories,
    ]


class SubCategoryAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = Subcategory
        icon = "fa-regular fa-folder-open"
        name = "Subcategory"
        label = "Subcategories"
        identity = None
        converter = None

        super().__init__(model, icon, name, label, identity, converter)

    fields = [
        Subcategory.id,
        Subcategory.name,
        Subcategory.category,
        Subcategory.service_options,
    ]


class ServiceOptionAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = ServiceOption
        icon = "fa-solid fa-wrench"
        name = "Service"
        label = "Services"
        identity = None
        converter = None

        super().__init__(model, icon, name, label, identity, converter)

    fields = [
        ServiceOption.id,
        ServiceOption.name,
        ServiceOption.subcategory,
        ServiceOption.icon,
    ]
