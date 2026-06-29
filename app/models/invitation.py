from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Invitation(Base):
    __tablename__ = "invitations"

    id: Mapped[int] = mapped_column(primary_key=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id")
    )

    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    receiver_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending"
    )
