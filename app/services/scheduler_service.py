from datetime import datetime, timedelta
from app.services.user import UserService
from app.services.company_member import CompanyMemberService
from app.services.quiz import QuizService
from app.services.notification import NotificationService
from app.models.quiz_attempt import QuizAttempt
from app.models.company_member import CompanyMember
from app.models.quiz import Quiz
from app.models.user import User

from sqlalchemy import select, func, and_, or_

class SchedulerService:
    @staticmethod
    async def check_quizzes(db):
            limit = datetime.utcnow() - timedelta(hours=24)

            stmt = (
                select(
                    User.id.label("user_id"),
                    Quiz.title.label("quiz_title"),
                    func.max(QuizAttempt.created_at).label("last_attempt"),
                )
                .join(
                    CompanyMember,
                    CompanyMember.user_id == User.id,
                )
                .join(
                    Quiz,
                    Quiz.company_id == CompanyMember.company_id,
                )
                .outerjoin(
                    QuizAttempt,
                    and_(
                        QuizAttempt.user_id == User.id,
                        QuizAttempt.quiz_id == Quiz.id,
                    ),
                )
                .group_by(
                    User.id,
                    Quiz.id,
                    Quiz.title,
                )
                .having(
                    or_(
                        func.max(QuizAttempt.created_at).is_(None),
                        func.max(QuizAttempt.created_at) < limit,
                    )
                )
            )

            result = await db.execute(stmt)

            for row in result:
                await NotificationService.create(
                    db,
                    row.user_id,
                    f'Please complete quiz "{row.quiz_title}"',
                )

            await db.commit()
