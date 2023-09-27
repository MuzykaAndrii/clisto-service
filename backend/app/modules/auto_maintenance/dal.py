from app.db.dal import BaseDAL
from backend.app.modules.auto_maintenance.models import Category, ServiceOption, Subcategory


class CategoryDAL(BaseDAL):
    model = Category


class SubcategoryDAL(BaseDAL):
    model = Subcategory


class ServiceOptionDAL(BaseDAL):
    model = ServiceOption