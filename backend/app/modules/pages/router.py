from fastapi import (
    APIRouter,
    Request,
)
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

templates = Jinja2Templates(directory=BASE_DIR / "app/templates")


@router.get("/main")
async def get_main_page(request: Request):
    return templates.TemplateResponse(
        name="main.html",
        context={"request": request},
    )
