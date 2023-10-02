from pydantic import (
    BaseModel,
    Field,
)


class UserLogin(BaseModel):
    username_or_email: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=8, max_length=30)
