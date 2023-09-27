from typing import (
    Any,
    Mapping,
)

from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.exc import NoResultFound

from app.db.session import async_session_maker


class BaseDAL:
    model = None

    @classmethod
    async def get_by_id(cls, id: int) -> Any | None:
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
    async def delete_by_id(cls, id: int) -> Any | NoResultFound:
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(cls.model.id == id).returning(cls.model)

            deleted_instance = await session.execute(stmt)
            return deleted_instance.scalar_one()

    @classmethod
    async def get_all(cls, offset: int = 0, limit: int = 50):
        async with async_session_maker() as session:
            stmt = select(cls.model).offset(offset).limit(limit)

            instances = await session.execute(stmt)
            return instances.all()
