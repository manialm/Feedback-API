from typing import Annotated

from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends

from auth.service import get_user, hash_password
from user.model import User

print(User)
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    admin = get_user(session, "admin")
    if not admin:
        admin = User(username="admin", password_hash=hash_password(b"admin"), is_admin=True)
        session.add(admin)
        session.commit()


def get_db():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
