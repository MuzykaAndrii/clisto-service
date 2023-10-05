from libcloud.storage.providers import get_driver
from libcloud.storage.types import Provider
from sqlalchemy_file.storage import StorageManager

from app.config import MEDIA_DIR


class IconsStorageManager:
    @staticmethod
    def init_manager() -> None:
        container = get_driver(Provider.LOCAL)(MEDIA_DIR).get_container(
            "services_icons"
        )
        StorageManager.add_storage("services-icons", container)
