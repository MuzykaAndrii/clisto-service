from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import DropDown
from starlette_admin.contrib.sqla import Admin
from starlette_admin.views import Link

from app.admin.auth_provider import AdminAuthProvider
from app.config import (
    BASE_DIR,
    settings,
)
from app.db.session import engine
from app.modules.appointments.admin.views import AppointmentAdminView
from app.modules.appointments.routes import router as appointments_router
from app.modules.auto_maintenance.admin.views import (
    CategoryAdminView,
    ServiceOptionAdminView,
    SubCategoryAdminView,
)
from app.modules.auto_maintenance.routes import router as maintenance_router
from app.modules.pages.routes import router as pages_router
from app.modules.users.admin.views import UserAdminView
from app.modules.users.services.user import UserService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    await UserService.ensure_admin_exists()

    yield
    # on shutdown


app = FastAPI(
    title="Clisto service",
    debug=settings.DEBUG,
    lifespan=lifespan,
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


admin = Admin(
    engine=engine,
    title="Admin panel",
    debug=settings.DEBUG,
    auth_provider=AdminAuthProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)],
)

admin.add_view(Link(label="Home Page", icon="fa-solid fa-house", url="/pages/main"))
admin.add_view(
    DropDown(
        "Maintenance",
        icon="fa-solid fa-wrench",
        views=[CategoryAdminView(), SubCategoryAdminView(), ServiceOptionAdminView()],
    )
)
admin.add_view(UserAdminView())
admin.add_view(AppointmentAdminView())

admin.mount_to(app)


app.mount("/static", StaticFiles(directory=BASE_DIR / "app/static"), name="static")


app.include_router(maintenance_router)
app.include_router(pages_router)
app.include_router(appointments_router)
