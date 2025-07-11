from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(index=True)


class User(UserBase, table=True):
    # TODO: | None?
    id: int | None = Field(default=None, primary_key=True)
    password_hash: bytes | None = Field(default=None)


class UserCreate(UserBase):
    password: bytes

class UserPublic(UserBase):
    id: int = Field(primary_key=True)
