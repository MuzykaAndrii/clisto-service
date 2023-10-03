from app.config import settings
from app.jwt.exceptions import (
    JWTExpiredError,
    JwtNotValidError,
)
from app.jwt.service import JwtService
from app.modules.users.dal import UserDAL
from app.modules.users.exceptions import (
    InvalidUserIdError,
    UserNotFoundError,
)
from app.modules.users.models import User
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

    @staticmethod
    async def get_user_from_token(token: str) -> User | None:
        try:
            payload: dict = JwtService.read_token(token)
        except JwtNotValidError:
            raise JwtNotValidError
        except JWTExpiredError:
            raise JWTExpiredError

        try:
            user_id = int(payload.get("sub"))
        except ValueError:
            raise InvalidUserIdError

        user: User = await UserDAL.get_by_id(user_id)
        if not user:
            raise UserNotFoundError

        return user

    @staticmethod
    def user_is_admin(user: User) -> bool:
        return user.is_superuser
