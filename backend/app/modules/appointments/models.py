from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as mc

from app.db.base import Base


class Appointment(Base):
    __tablename__ = "appointments_appointment"

    id: Mapped[int] = mc(primary_key=True)
    name: Mapped[str] = mc(String(50), nullable=False)
    email: Mapped[str] = mc(String(60), nullable=False)
    phone: Mapped[str] = mc(String(15), nullable=False)
    created_at: Mapped[datetime] = mc(default=datetime.utcnow)

    def __str__(self) -> str:
        return f"Appointment: from name: {self.name}, email: {self.email}, phone: {self.phone}, created_at: {self.created_at}"

    def __repr__(self) -> str:
        return f"Appointment(name={self.name}, email={self.email}, phone={self.phone}, created_at={self.created_at})"

    def __admin_repr__(self) -> str:
        return f"Appointment from: {self.email}, from {self.created_at}"
