from fastapi import APIRouter, HTTPException
from fastapi.params import Header


from user.service import get_user
from .service import check_password, create_user, create_jwt_token
from db import SessionDep
from user.model import UserCreate

router = APIRouter(prefix="/auth")


# TODO: is passing session to service clean code?
@router.post("/signup")
def signup(session: SessionDep, user: UserCreate):
    user_db = get_user(session, user.username)

    if user_db is None:
        return create_user(session, user)

    else:
        raise HTTPException(400, "Username already exists")


@router.post("/login")
def login(session: SessionDep, user: UserCreate):
    user_db = get_user(session, user.username)

    if user_db is None:
        raise HTTPException(404, "User not found")

    if check_password(user.password, user_db.password_hash):
        token = create_jwt_token({"sub": user_db.username})
        return {"access_token": token, "token_type": "bearer"}

    else:
        raise HTTPException(401, "Incorrect password")
