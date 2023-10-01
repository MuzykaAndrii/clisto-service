from typing import Iterable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.config import settings
from app.db.session import async_session_maker
from app.modules.auto_maintenance.dal import CategoryDAL
from app.modules.auto_maintenance.models import (
    Category,
    Subcategory,
)
from app.modules.auto_maintenance.schemas import CategorySchema

app = FastAPI(
    title="Clisto service",
    debug=settings.DEBUG,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.get("/ping")
async def pong():
    return {"response": "pong"}


@app.get("/test", response_model=list[CategorySchema])
async def some(offset: int = 0, limit: int = 10):
    async with async_session_maker() as session:
        stmt = (
            select(Category)
            .options(
                selectinload(Category.subcategories).selectinload(
                    Subcategory.service_options
                )
            )
            .offset(offset)
            .limit(limit)
        )

        result: Iterable[Category] = await session.scalars(stmt)

    return result
