from datetime import datetime, timedelta, UTC

from fastapi import HTTPException
from sqlmodel import Session, select
from user.model import User, UserCreate
from core.settings import settings

from fastapi.security import OAuth2PasswordBearer

import bcrypt
from jose import jwt
from jose.exceptions import JWTError


def create_user(session: Session, user: UserCreate):
    user_db = User.model_validate(user)
    user_db.password_hash = hash_password(user.password)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    token = create_jwt_token({"sub": user_db.username})
    return token


def hash_password(password: bytes):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password: bytes, hashed_password: bytes):
    return bcrypt.checkpw(password, hashed_password)


def create_jwt_token(payload: dict):
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {**payload, "exp": expire}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return token


def decode_jwt_token(token: bytes):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


# TODO: | None?
def get_user(session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    results = session.exec(statement)

    return results.first()
