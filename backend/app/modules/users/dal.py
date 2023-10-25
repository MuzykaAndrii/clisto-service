from typing import Iterable

from sqlalchemy import (
    or_,
    select,
)
from sqlalchemy.exc import NoResultFound

from app.db.dal import BaseDAL
from app.db.session import async_session_maker
from app.modules.users.models import User


class UserDAL(BaseDAL):
    model = User

    @classmethod
    async def get_user_by_email_or_username(cls, email_or_username: str) -> User | None:
        async with async_session_maker() as session:
            q = select(User).where(
                or_(User.email == email_or_username, User.username == email_or_username)
            )

            user = await session.execute(q)

            try:
                user = user.scalar_one()
            except NoResultFound:
                return None
            else:
                return user

    @classmethod
    async def get_admin_users(cls) -> Iterable[User] | None:
        admin_users: Iterable[User] | None = await cls.filter_by(is_superuser=True)
        return admin_users
