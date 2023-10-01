from typing import Iterable

from fastapi import APIRouter

from app.modules.auto_maintenance.dal import CategoryDAL
from app.modules.auto_maintenance.models import Category
from app.modules.auto_maintenance.schemas import CategorySchema

router = APIRouter(
    prefix="/services",
    tags=["Service"],
)


@router.get("/categories", response_model=list[CategorySchema], status_code=200)
async def get_categories():
    categories: Iterable[Category] = await CategoryDAL.get_all_with_related()

    return categories
