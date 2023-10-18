import smtplib
from email.message import EmailMessage
from smtplib import SMTPException

from app.config import settings


class SMTPService:
    host: str = settings.SMTP_HOST
    port: int = settings.SMTP_PORT
    user: str = settings.SMTP_USER
    password: str = settings.SMTP_PASSWORD

    @classmethod
    def send_emails(cls, *letters) -> None | SMTPException:
        with smtplib.SMTP_SSL(cls.host, cls.port) as smtp_server:
            smtp_server.login(cls.user, cls.password)

            for letter in letters:
                smtp_server.send_message(letter)

        return None
