from app.files.services import (
    FileService,
    MimeTypes,
)


class AppointmentImageService(FileService):
    max_file_size: int = 5 * 1024 * 1024
    expected_file_type: MimeTypes = MimeTypes.image
