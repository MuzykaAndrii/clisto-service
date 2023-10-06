from enum import Enum

from fastapi import UploadFile

from app.files.exceptions import (
    FileValidationError,
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
        mime_type, _ = file.content_type.split("/")
        return mime_type

    @staticmethod
    def get_file_mime_subtype(file: UploadFile):
        _, mime_subtype = file.content_type.split("/")
        return mime_subtype

    @staticmethod
    def get_file_size(file: UploadFile):
        return file.file.size

    @classmethod
    def validate_one(cls, file: UploadFile) -> None | FileValidationError:
        if cls.get_file_size(file) > cls.max_file_size:
            raise TooLargeFileError

        if cls.expected_file_type != cls.expected_file_type.value:
            raise InvalidMimeTypeError

    @classmethod
    def validate_bulk(cls, *files: tuple[UploadFile]) -> None | FileValidationError:
        if len(files) > cls.max_files_count:
            raise TooManyFilesError

        for file in files:
            cls.validate_one(file)
