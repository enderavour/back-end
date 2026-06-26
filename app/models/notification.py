from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped
import datetime
from app.db.base import Base
from typing import Any

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    message: Mapped[str] = mapped_column(String)

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    user: Mapped[Any] = relationship("User")
