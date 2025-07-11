from fastapi import FastAPI

from auth.controller import router as auth_router
from user.controller import router as user_router
from admin.controller import router as admin_router


app = FastAPI()


@app.get("/")
def index():
    return "FastAPI running"


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
