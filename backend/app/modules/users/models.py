from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(length=50), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    is_superuser = Column(Boolean, default=False, nullable=False)
