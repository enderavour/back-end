from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin

class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_visible: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    owner = relationship("User", back_populates="companies")

    quizzes = relationship(
        "Quiz",
        back_populates="company",
        cascade="all, delete-orphan"
    )
