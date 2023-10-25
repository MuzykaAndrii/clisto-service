from fastapi import UploadFile


class InvalidFileTypeError(Exception):
    pass


class MimeTypeHelper:
    def __init__(self, file: UploadFile):
        self._mime_type: str
        self._mime_subtype: str

        if not file.content_type:
            raise InvalidFileTypeError

        self._mime_type, self._mime_subtype = file.content_type.split("/")

    @property
    def mime_type(self) -> str:
        return self._mime_type

    @property
    def mime_subtype(self) -> str:
        return self._mime_subtype
