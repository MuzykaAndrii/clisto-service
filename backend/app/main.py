from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette_admin import DropDown
from starlette_admin.contrib.sqla import Admin
from starlette_admin.views import Link

from app.config import (
    BASE_DIR,
    settings,
)
from app.db.session import engine
from app.modules.auto_maintenance.admin.views import (
    CategoryAdminView,
    ServiceOptionAdminView,
    SubCategoryAdminView,
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


admin = Admin(
    engine=engine,
    title="Admin panel",
    debug=settings.DEBUG,
    # auth_provider=AdminAuthProvider(),
    # middlewares=[Middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)],
)

admin.add_view(Link(label="Home Page", icon="fa-solid fa-house", url="/pages/main"))
admin.add_view(
    DropDown(
        "Maintenance",
        icon="fa-solid fa-wrench",
        views=[CategoryAdminView(), SubCategoryAdminView(), ServiceOptionAdminView()],
    )
)

admin.mount_to(app)


app.mount("/static", StaticFiles(directory=BASE_DIR / "app/static"), name="static")


app.include_router(maintenance_router)
app.include_router(pages_router)
