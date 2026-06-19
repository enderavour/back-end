from this import s

from fastapi import HTTPException

from app.models.quiz import Quiz
from app.models.quiz import Question
from app.models.quiz import AnswerOption

from sqlalchemy import select

class QuizService:

    @staticmethod
    async def create_quiz(
        db,
        company_id,
        data
    ):
        if len(data.questions) < 2:
            raise HTTPException(
                400,
                "Quiz must contain at least 2 questions"
            )

        quiz = Quiz(
            title=data.title,
            description=data.description,
            company_id=company_id
        )

        db.add(quiz)

        await db.flush()

        for question_data in data.questions:
            if len(question_data.answers) < 2:
                raise HTTPException(
                    400,
                    "Question must contain atleast 2 answers"
                )

            question = Question(
                title=question_data.title,
                quiz_id=quiz.id
            )

            db.add(question)

            await db.flush()

            for answer_data in question_data.answers:

                answer = AnswerOption(
                    title=answer_data.title,
                    is_correct=answer_data.is_correct,
                    question_id=question.id
                )

                db.add(answer)

        await db.commit()
        await db.refresh(quiz)

        return quiz



    @staticmethod
    async def get_quiz(
        db,
        quiz_id
    ):
        result = await db.execute(
            select(Quiz).where(
                Quiz.id == quiz_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_company_quizzes(
        db,
        company_id,
        skip=0,
        limit=10
    ):
        result = await db.execute(
            select(Quiz)
            .where(Quiz.company_id == company_id)
            .offset(skip)
            .limit(limit)
        )

        return result.scalars().all()



    @staticmethod
    async def delete_quiz(
        db,
        quiz
    ):
        await db.delete(quiz)
        await db.commit()
