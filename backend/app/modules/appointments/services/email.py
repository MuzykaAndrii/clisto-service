from email.message import EmailMessage

from fastapi import UploadFile

from app.config import settings
from app.emails.services.mail import EmailService
from app.modules.appointments.models import Appointment
from app.template_engine.template_engine import TemplateEngine


class AppointmentEmailService:
    template_engine: TemplateEngine = TemplateEngine(
        "app/modules/appointments/letter_templates"
    )

    @classmethod
    def get_client_confirmation_letter(
        cls, client_name: str, client_email: str
    ) -> EmailMessage:
        letter_body = cls.template_engine.render_template(
            "client_confirmation.html",
            client_name=client_name,
        )

        letter = EmailService.create_letter(
            recipient=client_email,
            subject="Clisto service appointment feedback",
            content=letter_body,
        )

        return letter

    @classmethod
    async def get_notification_letters(
        cls,
        appointment: Appointment,
        images: list[UploadFile],
    ) -> list[EmailMessage]:
        letter_body = cls.template_engine.render_template(
            "new_appointment_notification.html",
            id=appointment.id,
            name=appointment.name,
            email=appointment.email,
            phone=appointment.phone,
        )

        letters: list = []

        for recipient in settings.APPOINTMENTS_RECEIVERS:
            letter = await EmailService.create_letter_with_files(
                recipient=recipient,
                subject="New appointment received",
                content=letter_body,
                files=images,
            )
            letters.append(letter)

        return letters
