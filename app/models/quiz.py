from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin

class Quiz(Base, TimestampMixin):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id")
    )

    company = relationship("Company", back_populates="quizzes")

    questions = relationship(
        "Question",
        cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))

    quiz_id: Mapped[int] = mapped_column(
        ForeignKey("quizzes.id")
    )

    quiz = relationship("Quiz")

    answers = relationship(
        "AnswerOption",
        cascade="all, delete-orphan"
    )

class AnswerOption(Base):
    __tablename__ = "answer_options"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))

    is_correct: Mapped[bool] = mapped_column(default=False)

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id")
    )
