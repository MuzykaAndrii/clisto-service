from typing import Annotated

from fastapi import (
    APIRouter,
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
from app.modules.appointments.services.email import AppointmentEmailService
from app.modules.appointments.services.image import AppointmentImageService
from app.template_engine.services import TemplateEngineService

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
):
    try:
        for image in images:
            AppointmentImageService(image).validate()
    except TooLargeFileError:
        raise HTTPException(413, detail="Uploaded image should be smaller than 5mb")
    except InvalidMimeTypeError:
        raise HTTPException(415, detail="Uploaded files should be images")

    new_appointment = await AppointmentDAL.create(name=name, email=email, phone=phone)

    client_letter = AppointmentEmailService.get_client_confirmation_letter(
        new_appointment.name,
        new_appointment.email,
    )

    notification_letters = await AppointmentEmailService.get_notification_letters(
        appointment=new_appointment,
        images=images,
    )
    SMTPService.send_emails(client_letter, *notification_letters)

    return {"status": "success"}
