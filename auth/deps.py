from typing import Annotated
from fastapi import Depends, HTTPException, Header, status

from db import SessionDep
from user.model import User, UserPublic

from .service import decode_jwt_token
from user.service import get_user


def get_authorization_token(authorization: Annotated[str, Header()]) -> bytes:
    bearer, token = authorization.split()
    return token


def get_current_user(
    session: SessionDep, token: Annotated[bytes, Depends(get_authorization_token)]
):
    payload = decode_jwt_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload["sub"]
    user = get_user(session, username)

    if not user:
        raise HTTPException(404, "User not found")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_user_admin(current_user: CurrentUser):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin privileges required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


CurrentUserAdmin = Annotated[User, Depends(get_current_user_admin)]
