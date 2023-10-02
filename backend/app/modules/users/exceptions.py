class UserError(Exception):
    pass


class UserLoginError(UserError):
    pass


class UserNotFoundError(UserLoginError):
    pass


class UserInvalidPassword(UserLoginError):
    pass


class JwtNotValidError(Exception):
    pass


class JWTExpiredError(Exception):
    pass
