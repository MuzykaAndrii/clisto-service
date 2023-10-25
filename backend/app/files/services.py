from enum import Enum

from fastapi import UploadFile

from app.files.exceptions import (
    FileValidationError,
    InvalidFileNameError,
    InvalidMimeTypeError,
    TooLargeFileError,
    TooManyFilesError,
)


class MimeTypes(Enum):
    image = "image"
    audio = "audio"
    video = "video"
    text = "text"
    application = "application"


class FileService:
    # TODO: move validation logic to pydantic schema
    max_file_size: int
    expected_file_type: MimeTypes
    max_files_count: int

    @staticmethod
    def get_file_mime_type(file: UploadFile):
        if not file.content_type:
            raise InvalidFileNameError

        mime_type, _ = file.content_type.split("/")
        return mime_type

    @staticmethod
    def get_file_mime_subtype(file: UploadFile):
        if not file.content_type:
            raise InvalidFileNameError

        _, mime_subtype = file.content_type.split("/")
        return mime_subtype

    @staticmethod
    def get_file_size(file: UploadFile):
        return file.size

    @classmethod
    def validate_one(cls, file: UploadFile) -> None | FileValidationError:
        if cls.get_file_size(file) > cls.max_file_size:
            raise TooLargeFileError

        if cls.get_file_mime_type(file) != cls.expected_file_type.value:
            raise InvalidMimeTypeError

        return None

    @classmethod
    def validate_bulk(cls, *files) -> None | FileValidationError:
        if len(files) > cls.max_files_count:
            raise TooManyFilesError

        for file in files:
            cls.validate_one(file)

        return None
