from fastapi import APIRouter
from sqlmodel import select, func

from db import SessionDep
from feedback.model import Feedback

router = APIRouter(prefix="")


@router.get("/")
def index():
    return "App is running\n"


@router.get("/feedback/summary")
def summary(session: SessionDep):
    feedback_count = session.exec(select(func.count(Feedback.id))).one()

    feedback_avg = (
        session.exec(select(func.sum(Feedback.rating))).one() / feedback_count
    )

    return {"count": feedback_count, "average": feedback_avg}
