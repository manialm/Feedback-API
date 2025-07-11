from typing import Annotated
from fastapi import APIRouter, Body
from sqlmodel import select

from admin.model import UserPrivate, UserUpdate
from auth.deps import CurrentUserAdmin
from auth.service import hash_password
from feedback.model import Feedback
from user.service import get_user_by_id
from db import SessionDep
from user.model import User, UserCreate

router = APIRouter(prefix="/admin")


@router.get("/users", response_model=list[UserPrivate])
def users(admin: CurrentUserAdmin, session: SessionDep):
    statement = select(User)
    results = session.exec(statement)
    return list(results)


# TODO: invalidate tokens createdj before patch?
@router.patch("/users/{id}", response_model=UserPrivate)
def update_user(admin: CurrentUserAdmin, session: SessionDep, user_update: UserUpdate, id: int):
    user = get_user_by_id(session, id)


    user_dump = user_update.model_dump(exclude_unset=True)
    password = user_dump.get("password")
    update = {"password_hash": hash_password(password)} if password else None

    user.sqlmodel_update(user_dump, update=update)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/feedback")
def feedbacks(admin: CurrentUserAdmin, session: SessionDep):
    statement = select(Feedback)
    results = session.exec(statement)
    return list(results)


# NOTE: Body(embed=True) expects { "is_admin": true }
@router.patch("/roles/{user_id}")
def change_role(
    admin: CurrentUserAdmin,
    session: SessionDep,
    user_id: int,
    is_admin: Annotated[bool, Body(embed=True)],
):
    user = get_user_by_id(session, user_id)

    if is_admin is not None:
        user.is_admin = is_admin
        session.add(user)
        session.commit()
        session.refresh(user)

    return user
