from fastapi import APIRouter

from auth.deps import CurrentUser
from user.model import UserPublic

router = APIRouter(prefix="/user")


@router.get("/profile", response_model=UserPublic)
def get(current_user: CurrentUser):
    return current_user
