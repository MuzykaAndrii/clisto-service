import mimetypes
from enum import Enum

from fastapi import UploadFile

from app.files.exceptions import (
    FileValidationError,
    InvalidMimeTypeError,
    TooLargeFileError,
)


class MimeTypes(Enum):
    image = "image"
    audio = "audio"
    video = "video"
    text = "text"
    application = "application"


class FileService:
    max_file_size: int
    expected_file_type: MimeTypes

    def __init__(self, file: UploadFile) -> None:
        self.file = file
        self._mime_type, self._mime_subtype = file.content_type.split("/")

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def mime_subtype(self):
        return self._mime_subtype

    @property
    def file_size(self):
        return self.file.size

    def validate(self) -> None | FileValidationError:
        if self.file_size > self.max_file_size:
            raise TooLargeFileError

        if self.mime_type != self.expected_file_type.value:
            raise InvalidMimeTypeError
