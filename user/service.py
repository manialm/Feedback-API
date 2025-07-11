from sqlmodel import select
from db import SessionDep
from user.model import User


# TODO: | None?
def get_user(session: SessionDep, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    results = session.exec(statement)

    return results.first()


def get_user_by_id(session: SessionDep, id: int):
    statement = select(User).where(User.id == id)
    results = session.exec(statement)

    return results.first()
