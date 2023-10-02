from app.modules.users.dal import UserDAL
from app.modules.users.exceptions import (
    UserInvalidPassword,
    UserNotFoundError,
)
from app.modules.users.models import User
from app.modules.users.schemas import UserLogin
from app.modules.users.services.password import PWDService


class AuthService:
    @staticmethod
    async def authenticate_user(user_in: UserLogin) -> User:
        user = await UserDAL.get_user_by_email_or_username(user_in.username_or_email)

        if not user:
            raise UserNotFoundError

        pass_matching = PWDService.verify_password(
            raw_password=user_in.password, hashed_password=user.password_hash
        )

        if not pass_matching:
            raise UserInvalidPassword

        return user
