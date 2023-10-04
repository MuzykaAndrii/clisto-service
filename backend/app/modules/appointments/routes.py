from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
)

from app.emails.services.mail import EmailService
from app.emails.services.smtp import SMTPService
from app.files.exceptions import (
    FileValidationError,
    InvalidMimeTypeError,
    TooLargeFileError,
)
from app.modules.appointments.forms import AppointmentForm
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

    letter = await EmailService.create_letter_with_files(
        recipient=email,
        subject="Test email with files",
        content=f"Mock content from {name} {phone}",
        files=images,
    )
    SMTPService.send_email(letter)

    return {"status": "success"}
