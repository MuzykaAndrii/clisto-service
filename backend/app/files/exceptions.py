class FileValidationError(Exception):
    pass


class InvalidFileNameError(FileValidationError):
    pass


class TooLargeFileError(FileValidationError):
    pass


class TooManyFilesError(FileValidationError):
    pass


class InvalidMimeTypeError(FileValidationError):
    pass
