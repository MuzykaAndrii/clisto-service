from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.config import settings

if settings.MODE == "TEST":
    engine = create_async_engine(settings.test_database_url, poolclass=NullPool)
else:
    engine = create_async_engine(settings.database_url)


async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
