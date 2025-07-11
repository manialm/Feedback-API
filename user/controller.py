from fastapi import APIRouter

from auth.deps import CurrentUser
from db import SessionDep
from feedback.model import Feedback, FeedbackCreate
from user.model import UserPublic

router = APIRouter(prefix="/user")


@router.get("/profile", response_model=UserPublic)
def get(current_user: CurrentUser):
    return current_user


@router.post("/feedback")
def send_feedback(
    session: SessionDep, current_user: CurrentUser, feedback: FeedbackCreate
):
    feedback_db = Feedback.model_validate(feedback, update={"user_id": current_user.id})

    session.add(feedback_db)
    session.commit()
    session.refresh(feedback_db)

    return feedback_db
