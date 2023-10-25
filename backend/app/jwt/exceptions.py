class JwtError(Exception):
    pass


class JwtMissingError(JwtError):
    pass


class JwtNotValidError(JwtError):
    pass


class JWTExpiredError(JwtError):
    pass
