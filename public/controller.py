from fastapi import APIRouter
from sqlmodel import select, func

from db import SessionDep
from feedback.model import Feedback

router = APIRouter(prefix="")


@router.get("/")
def index():
    return "App is running"


@router.get("/feedback/summary")
def summary(session: SessionDep):
    feedback_count = session.exec(select(func.count(Feedback.id))).one()

    feedback_sum = (
        session.exec(select(func.sum(Feedback.rating))).one()
    )

    feedback_avg = feedback_sum / feedback_count if feedback_sum else 0

    if not feedback_count:
        feedback_count = 0

    return {"count": feedback_count, "average": feedback_avg}
