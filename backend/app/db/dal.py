from abc import ABC
from typing import (
    Iterable,
    Mapping,
)

from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.exc import NoResultFound

from app.db.base import Base as DbModel
from app.db.session import async_session_maker


class BaseDAL(ABC):
    model: type[DbModel]

    @classmethod
    async def get_by_id(cls, id: int) -> DbModel | None:
        async with async_session_maker() as session:
            result = await session.get(cls.model, id)

            if not result:
                return None
            return result

    @classmethod
    async def create(cls, **fields: Mapping):
        async with async_session_maker() as session:
            instance = cls.model(**fields)

            session.add(instance)
            await session.commit()
            await session.refresh(instance)

            return instance

    @classmethod
    async def delete_by_id(cls, id: int) -> DbModel | NoResultFound:
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(cls.model.id == id).returning(cls.model)

            deleted_instance = await session.execute(stmt)
            return deleted_instance.scalar_one()

    @classmethod
    async def get_all(
        cls, offset: int = 0, limit: int = 50
    ) -> Iterable[DbModel] | None:
        async with async_session_maker() as session:
            stmt = select(cls.model).offset(offset).limit(limit)

            instances = await session.execute(stmt)
            return instances.scalars().all()

    @classmethod
    async def filter_by(cls, **filter_criteria: Mapping) -> Iterable[DbModel] | None:
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(**filter_criteria)

            filter_result = await session.scalars(stmt)
            return filter_result.all()
