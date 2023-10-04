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
    """
    TODO:
        1. Validate files size and type:

            if len(files) > MAX_FILES_COUNT:
                raise TooManyFilesError
            if file.size > max_file_size:
                raise TooLargeFileError
            if file.type != expected_file_types:
                raise WrongFileFormat

        2. Send letters:
            sended = letter_to_owner.send

            if not sended:
                fail_letter_to_client.send
            else:
                success_letter_to_client.send

        3. Save appointment to database:
            appointment.save

    """
    try:
        for image in images:
            AppointmentImageService(image).validate()
    except TooLargeFileError:
        raise HTTPException(413, detail="Uploaded image should be smaller than 5mb")
    except InvalidMimeTypeError:
        raise HTTPException(415, detail="Uploaded files should be images")

    client_letter = AppointmentEmailService.get_client_confirmation_letter(name, email)
    SMTPService.send_emails(client_letter)

    return {"status": "success"}
