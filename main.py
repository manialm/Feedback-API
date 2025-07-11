from fastapi import FastAPI
from sqlmodel import Session, SQLModel

from db import engine, User
from auth.controller import router as auth_router
from user.controller import router as user_router

SQLModel.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
