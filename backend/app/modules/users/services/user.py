from app.config import settings
from app.modules.users.dal import UserDAL
from app.modules.users.services.password import PWDService


class UserService:
    @staticmethod
    async def create_base_admin_user() -> None:
        await UserDAL.create(
            username=settings.BASE_ADMIN_NAME,
            email=settings.BASE_ADMIN_EMAIL,
            password_hash=PWDService.get_password_hash(settings.BASE_ADMIN_PASS),
            is_superuser=True,
        )
