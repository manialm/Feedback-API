from fastapi import APIRouter
from sqlmodel import select

from auth.deps import CurrentUserAdmin
from db import SessionDep
from user.model import User

router = APIRouter(prefix="/admin")

@router.get("/users")
def users(admin: CurrentUserAdmin, session: SessionDep):
    statement = select(User)
    results = session.exec(statement)
    return list(results)