from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.dal import BaseDAL
from app.db.session import async_session_maker
from app.modules.auto_maintenance.models import (
    Category,
    ServiceOption,
    Subcategory,
)


class CategoryDAL(BaseDAL):
    model = Category

    @classmethod
    async def get_all_with_related(cls):
        async with async_session_maker() as session:
            stmt = select(Category).options(
                selectinload(Category.subcategories).selectinload(
                    Subcategory.service_options
                )
            )

            categories: Iterable[Category] = await session.scalars(stmt)
            return categories


class SubcategoryDAL(BaseDAL):
    model = Subcategory


class ServiceOptionDAL(BaseDAL):
    model = ServiceOption
