from sqlalchemy import select
from app.models.quiz import Quiz

class QuizRepository:
    @staticmethod
    async def get_quiz_by_title(db, company_id, quiz_title):
        result = await db.execute(
            select(Quiz).where(
                Quiz.company_id == company_id,
                Quiz.title == quiz_title
            )
        )

        return result.scalar_one_or_none()
