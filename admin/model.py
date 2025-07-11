from user.model import UserPublic
from sqlmodel import Field, SQLModel


class Admin(UserPublic):
    pass


class UserPrivate(UserPublic):
    is_admin: bool


class UserUpdate(SQLModel):
    username: str | None = Field(default=None)
    password: bytes | None = Field(default=None)
