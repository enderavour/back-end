from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String

class CompanyMember(Base):
    __tablename__ = "company_members"

    id: Mapped[int] = mapped_column(primary_key=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    role = mapped_column(
        String(50),
        default="member"
    )
