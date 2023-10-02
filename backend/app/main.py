from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import (
    BASE_DIR,
    settings,
)
from app.modules.auto_maintenance.routes import router as maintenance_router
from app.modules.pages.routes import router as pages_router

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

app.mount("/static", StaticFiles(directory=BASE_DIR / "app/static"), name="static")


app.include_router(maintenance_router)
app.include_router(pages_router)
