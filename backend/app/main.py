from typing import Iterable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
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


@app.get("/categories", response_model=list[CategorySchema], status_code=200)
async def get_categories():
    categories: Iterable[Category] = await CategoryDAL.get_all_with_related()

    return categories
