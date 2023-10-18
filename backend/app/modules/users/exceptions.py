class UserError(Exception):
    pass


class InvalidUserIdError(UserError):
    pass


class UserLoginError(UserError):
    pass


class UserNotFoundError(UserLoginError):
    pass


class UserInvalidPassword(UserLoginError):
    pass
