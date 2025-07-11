from fastapi import FastAPI
from sqlmodel import SQLModel, Session

from auth.controller import router as auth_router
from user.controller import router as user_router
from admin.controller import router as admin_router
from public.controller import router as public_router

from auth.service import hash_password
from user.service import get_user
from user.model import User

from db import engine


app = FastAPI()


# create admin user if it doesn't exist
with Session(engine) as session:
    admin = get_user(session, "admin")
    if not admin:
        admin = User(
            username="admin", password_hash=hash_password(b"admin"), is_admin=True
        )
        session.add(admin)
        session.commit()


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(public_router)
