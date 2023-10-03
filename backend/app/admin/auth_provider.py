from fastapi import (
    Request,
    Response,
)
from pydantic import ValidationError
from starlette_admin.auth import (
    AdminUser,
    AuthProvider,
)
from starlette_admin.exceptions import (
    FormValidationError,
    LoginFailed,
)

from app.jwt.exceptions import (
    JWTExpiredError,
    JwtMissingError,
    JwtNotValidError,
)
from app.jwt.service import JwtService
from app.modules.users.dal import UserDAL
from app.modules.users.exceptions import (
    InvalidUserIdError,
    UserInvalidPassword,
    UserNotFoundError,
)
from app.modules.users.models import User
from app.modules.users.schemas import UserLogin
from app.modules.users.services.auth import AuthService
from app.modules.users.services.user import UserService


class AdminAuthProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        try:
            credentials = UserLogin(
                username_or_email=username,
                password=password,
            )
        except ValidationError:
            raise FormValidationError({"failed": "Invalid input data"})

        try:
            user = await AuthService.authenticate_user(credentials)
        except UserNotFoundError:
            raise LoginFailed("Invalid username/email")
        except UserInvalidPassword:
            raise LoginFailed("Invalid password")

        auth_token = JwtService.create_token(str(user.id))
        request.session.update({"admin_token": auth_token})
        return response

    async def is_authenticated(self, request: Request) -> bool:
        token: str = request.session.get("admin_token")

        try:
            current_user = await UserService.get_user_from_token(token)
        except (
            JwtMissingError,
            JwtNotValidError,
            JWTExpiredError,
            InvalidUserIdError,
            UserNotFoundError,
        ):
            return False

        if not UserService.user_is_admin(current_user):
            return False

        request.state.user = current_user
        return True

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user

        return AdminUser(username=user.username)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
