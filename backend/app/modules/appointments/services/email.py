from email.message import EmailMessage

from jinja2 import Environment

from app.emails.services.mail import EmailService
from app.template_engine.services import TemplateEngineService


class AppointmentEmailService:
    template_engine: Environment = TemplateEngineService.get_engine(
        "app/modules/appointments/letter_templates"
    )
    client_confirmation_template: str = "client_confirmation.html"
    performer_letter_template: str = "new_appointment_notification.html"

    @classmethod
    def get_client_confirmation_letter(
        cls, client_name: str, client_email: str
    ) -> EmailMessage:
        body_template = cls.template_engine.get_template(
            cls.client_confirmation_template
        )

        message_body = body_template.render(client_name=client_name)

        letter = EmailService.create_letter(
            recipient=client_email,
            subject="Clisto service appointment feedback",
            content=message_body,
        )

        return letter
