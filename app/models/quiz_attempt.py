from app.db.base import Base
from app.db.mixins import TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime

class QuizAttempt(Base, TimestampMixin):
    __tablename__ = "quiz_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))

    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    correct_answers: Mapped[int]
    total_questions: Mapped[int]
