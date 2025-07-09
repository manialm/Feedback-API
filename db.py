from typing import Annotated

from sqlmodel import create_engine, Session
from fastapi import Depends

from user.model import User

print(User)
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def get_db():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
