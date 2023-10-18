from passlib.context import CryptContext


class PWDService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        password_hash: str = cls.pwd_context.hash(password)
        return password_hash

    @classmethod
    def verify_password(cls, raw_password: str, hashed_password: str) -> bool:
        is_passwords_matches: bool = cls.pwd_context.verify(
            raw_password, hashed_password
        )
        return is_passwords_matches
