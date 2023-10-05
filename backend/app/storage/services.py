from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager

from app.config import MEDIA_DIR


class StorageService:
    @classmethod
    def init_storage(
        cls, container_name: str, storage_name: str, *args, **kwargs
    ) -> None:
        container = LocalStorageDriver(*args, **kwargs).get_container(
            container_name,
        )
        StorageManager.add_storage(storage_name, container)


class MediaStorageService(StorageService):
    @classmethod
    def init_storage(cls, container_name: str, storage_name: str) -> None:
        super().init_storage(container_name, storage_name, MEDIA_DIR)
