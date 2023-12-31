from app.files.services import (
    FileService,
    MimeTypes,
)


class AppointmentImageService(FileService):
    max_file_size: int = 10 * 1024 * 1024
    expected_file_type: MimeTypes = MimeTypes.image
    max_files_count: int = 10
