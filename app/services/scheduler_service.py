from datetime import datetime, timedelta
from app.services.user import UserService
from app.services.company_member import CompanyMemberService
from app.services.quiz import QuizService
from app.services.notification import NotificationService
from app.models.quiz_attempt import QuizAttempt

from sqlalchemy import select, func

class SchedulerService:
    @staticmethod
    async def check_quizzes(db):
        users = await UserService.get_users(db, skip=0, limit=1000)

        now = datetime.utcnow()
        limit = now - timedelta(hours=24)

        for user in users:
            companies = await CompanyMemberService.get_user_companies(db, user.id)

            for member in companies:
                company_id = member.company_id

                quizzes = await QuizService.get_company_quizzes(
                    db,
                    company_id,
                    skip=0,
                    limit=10000
                )

                for quiz in quizzes:
                    result = await db.execute(
                        select(func.max(QuizAttempt.created_at)).where(
                            QuizAttempt.user_id == user.id,
                            QuizAttempt.quiz_id == quiz.id
                        )
                    )

                    last_attempt = result.scalar()

                    if last_attempt is None or last_attempt < limit:
                        await NotificationService.create(
                            db,
                            user.id,
                            f'Please complete quiz "{quiz.title}"'
                        )

        await db.commit()
