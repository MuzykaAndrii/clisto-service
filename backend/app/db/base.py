from sqlalchemy import Integer
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
)
from sqlalchemy.orm import mapped_column as mc


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mc(Integer, primary_key=True)
