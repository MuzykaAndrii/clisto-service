from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    HTTPException,
    UploadFile,
)

from app.emails.services.smtp import SMTPService
from app.files.exceptions import (
    InvalidMimeTypeError,
    TooLargeFileError,
    TooManyFilesError,
)
from app.modules.appointments.forms import AppointmentForm
from app.modules.appointments.services.appointment import AppointmentService

router = APIRouter(
    prefix="/appointments",
    tags=["Appointment"],
)


@router.post("/make_appointment")
async def make_appointment(
    name: Annotated[str, AppointmentForm.name_filed],
    email: Annotated[str, AppointmentForm.email_filed],
    phone: Annotated[str, AppointmentForm.phone_filed],
    images: list[UploadFile],
    bg_tasks: BackgroundTasks,
):
    try:
        letters = AppointmentService.make_appointment(name, email, phone, images)
    except TooLargeFileError:
        raise HTTPException(413, detail="Uploaded image should be smaller than 10mb")
    except InvalidMimeTypeError:
        raise HTTPException(415, detail="Uploaded files should be images")
    except TooManyFilesError:
        raise HTTPException(413, detail="Too many files uploaded, expected up to 10")

    bg_tasks.add_task(
        SMTPService.send_emails,
        *letters,
    )

    return {"status": "success"}
