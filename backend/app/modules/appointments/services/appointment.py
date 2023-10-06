from email.message import EmailMessage

from app.files.exceptions import FileValidationError
from app.modules.appointments.dal import AppointmentDAL
from app.modules.appointments.models import Appointment
from app.modules.appointments.services.email import AppointmentEmailService
from app.modules.appointments.services.image import AppointmentImageService


class AppointmentService:
    @staticmethod
    async def make_appointment(name, email, phone, images) -> list[EmailMessage]:
        try:
            AppointmentImageService.validate_bulk(*images)
        except FileValidationError as e:
            raise e

        new_appointment: Appointment = await AppointmentDAL.create(
            name=name,
            email=email,
            phone=phone,
        )

        client_letter = AppointmentEmailService.get_client_confirmation_letter(
            client_name=new_appointment.name,
            client_email=new_appointment.email,
        )

        notification_letters = await AppointmentEmailService.get_notification_letters(
            appointment=new_appointment,
            images=images,
        )

        letters = [client_letter, *notification_letters]
        return letters
