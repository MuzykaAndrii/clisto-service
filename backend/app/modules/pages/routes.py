from collections import defaultdict
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Form,
    Request,
    UploadFile,
)
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.config import BASE_DIR
from app.emails.services.smtp import SMTPService
from app.files.exceptions import (
    InvalidMimeTypeError,
    TooLargeFileError,
    TooManyFilesError,
)
from app.modules.appointments.services.appointment import AppointmentService
from app.modules.auto_maintenance.routes import get_categories
from app.modules.pages.schemas import CreateAppointmentSchema

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
            "categories": categories.all(),
            "errors": None,
        },
    )


@router.post("/main")
async def make_appointment(
    request: Request,
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    bg_tasks: BackgroundTasks,
    images: list[UploadFile],
    categories=Depends(get_categories),
):
    errors: dict[str, list] = defaultdict(list)

    try:
        CreateAppointmentSchema(name=name, email=email, phone=phone)
    except ValidationError as e:
        for error in e.errors():
            for error_location in error.get("loc"):
                errors[error_location].append(error.get("msg"))

    try:
        letters = await AppointmentService.make_appointment(name, email, phone, images)
    except TooLargeFileError:
        errors["photos"].append("Too large image sended, please send images up to 10mb")
    except InvalidMimeTypeError:
        errors["photos"].append("Invalid file type, please send only images")
    except TooManyFilesError:
        errors["photos"].append("Allowed to send up to 10 images at once")

    if not errors:
        bg_tasks.add_task(
            SMTPService.send_emails,
            *letters,
        )

    return templates.TemplateResponse(
        name="main.html",
        context={
            "request": request,
            "categories": categories.all(),
            "errors": errors,
            "success": not bool(errors),
        },
    )
