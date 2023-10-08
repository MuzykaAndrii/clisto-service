from pydantic import (
    BaseModel,
    Field,
)


class CreateAppointmentSchema(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    phone: str = Field(pattern=r"^[0-9+\s\-]{1,20}$")
