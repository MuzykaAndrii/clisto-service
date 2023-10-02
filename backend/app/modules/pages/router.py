from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

templates = Jinja2Templates(directory=BASE_DIR / "app/templates")
