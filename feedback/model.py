from sqlmodel import CheckConstraint, Field, SQLModel


class FeedbackBase(SQLModel):
    # TODO: add bounds to rating
    rating: int | None = Field(default=1)
    comment: str | None = Field(max_length=256)


class Feedback(FeedbackBase, table=True):
    id: int | None = Field(primary_key=True, default=None)
    user_id: int | None = Field(foreign_key="user.id")


class FeedbackCreate(FeedbackBase):
    pass
