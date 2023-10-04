from email.message import EmailMessage

from fastapi import UploadFile

from app.config import settings
from app.emails.utils import MimeTypeHelper


class EmailService:
    @classmethod
    def create_letter(cls, recipient: str, subject: str, content: str) -> EmailMessage:
        letter = EmailMessage()

        letter["subject"] = subject
        letter["From"] = settings.SMTP_USER
        letter["To"] = recipient
        letter.set_content(content, subtype="html")

        return letter

    @classmethod
    async def attach_file_to_letter(
        cls, letter: EmailMessage, file: UploadFile
    ) -> EmailMessage:
        mime_helper = MimeTypeHelper(file)

        letter.add_attachment(
            await file.read(),
            maintype=mime_helper.mime_type,
            subtype=mime_helper.mime_subtype,
            filename=file.filename,
        )
        await file.close()
        return letter

    @classmethod
    async def create_letter_with_files(
        cls, recipient: str, subject: str, content: str, files: list[UploadFile]
    ) -> EmailMessage:
        letter = cls.create_letter(recipient, subject, content)

        for file in files:
            letter = await cls.attach_file_to_letter(letter, file)

        return letter
