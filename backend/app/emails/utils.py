from fastapi import UploadFile


class MimeTypeHelper:
    def __init__(self, file: UploadFile):
        self._mime_type, self._mime_subtype = file.content_type.split("/")

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def mime_subtype(self):
        return self._mime_subtype
