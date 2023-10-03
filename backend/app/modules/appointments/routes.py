from typing import Annotated

from fastapi import (
    APIRouter,
    UploadFile,
)

from app.emails.services.mail import EmailService
from app.emails.services.smtp import SMTPService
from app.modules.appointments.forms import AppointmentForm

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
    letter = await EmailService.create_letter_with_files(
        recipient=email,
        subject="Test email with files",
        content=f"Mock content from {name} {phone}",
        files=images,
    )
    SMTPService.send_email(letter)

    return {"status": "success"}
