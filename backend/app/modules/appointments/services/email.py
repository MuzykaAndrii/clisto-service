from email.message import EmailMessage
from typing import Mapping

from fastapi import UploadFile
from jinja2 import Environment

from app.config import settings
from app.emails.services.mail import EmailService
from app.modules.appointments.models import Appointment
from app.template_engine.services import TemplateEngineService


class AppointmentEmailService:
    template_engine: Environment = TemplateEngineService.get_engine(
        "app/modules/appointments/letter_templates"
    )
    client_confirmation_template: str = "client_confirmation.html"
    notification_letter_template: str = "new_appointment_notification.html"

    @classmethod
    def _render_template(cls, template_name: str, **fields: Mapping):
        body_template = cls.template_engine.get_template(template_name)

        content = body_template.render(**fields)

        return content

    @classmethod
    def get_client_confirmation_letter(
        cls, client_name: str, client_email: str
    ) -> EmailMessage:
        letter_body = cls._render_template(
            cls.client_confirmation_template, client_name=client_name
        )

        letter = EmailService.create_letter(
            recipient=client_email,
            subject="Clisto service appointment feedback",
            content=letter_body,
        )

        return letter

    @classmethod
    async def get_notification_letters(
        cls, appointment: Appointment, images: list[UploadFile]
    ) -> list[EmailMessage]:
        letter_body = cls._render_template(
            cls.notification_letter_template,
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
