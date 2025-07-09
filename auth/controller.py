from fastapi import APIRouter, HTTPException
from db import SessionDep
from user.model import UserCreate

from .service import create_user

router = APIRouter(prefix="/auth")

#TODO: is passing session to service clean code?
@router.post("/signup")
def signup(session: SessionDep, user: UserCreate):
    return create_user(session, user)

@router.post("/login")
def login(session: SessionDep, user: UserCreate):
    return ""