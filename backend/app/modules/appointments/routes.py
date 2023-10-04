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
)
from app.modules.appointments.dal import AppointmentDAL
from app.modules.appointments.forms import AppointmentForm
from app.modules.appointments.models import Appointment
from app.modules.appointments.services.email import AppointmentEmailService
from app.modules.appointments.services.image import AppointmentImageService

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
        for image in images:
            AppointmentImageService(image).validate()
    except TooLargeFileError:
        raise HTTPException(413, detail="Uploaded image should be smaller than 5mb")
    except InvalidMimeTypeError:
        raise HTTPException(415, detail="Uploaded files should be images")

    new_appointment: Appointment = await AppointmentDAL.create(
        name=name, email=email, phone=phone
    )

    client_letter = AppointmentEmailService.get_client_confirmation_letter(
        new_appointment.name,
        new_appointment.email,
    )

    notification_letters = await AppointmentEmailService.get_notification_letters(
        appointment=new_appointment,
        images=images,
    )

    letters_to_send = [client_letter, *notification_letters]

    bg_tasks.add_task(
        SMTPService.send_emails,
        *letters_to_send,
    )

    return {"status": "success"}
