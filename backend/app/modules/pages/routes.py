from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR
from app.modules.auto_maintenance.routes import get_categories

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

templates = Jinja2Templates(directory=BASE_DIR / "app/templates")


@router.get("/main")
async def get_main_page(
    request: Request,
    categories=Depends(get_categories),
):
    return templates.TemplateResponse(
        name="main.html",
        context={
            "request": request,
            "categories": categories,
        },
    )
