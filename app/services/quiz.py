from fastapi import HTTPException

from app.models.quiz import Quiz
from app.models.quiz import Question
from app.models.quiz import AnswerOption
from app.models.quiz_attempt import QuizAttempt
from app.models.user_answer import UserAnswer
from .redis_service import RedisQuizService
from app.services.company_member import CompanyMemberService
from .notification import NotificationService
from app.models.notification import Notification


from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
import datetime

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

        members = await CompanyMemberService.get_company_members(db, quiz.company_id)

        notifications = []

        for member in members:
            notifications.append(
                Notification(
                    user_id=m.user_id,
                    message=f'New quiz "{quiz.title} is available"'
                )
                for m in members
            )

        db.add_all(notifications)

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

    @staticmethod
    async def take_quiz(db, quiz, user, answers):
        result = await db.execute(
            select(Quiz)
            .options(
                selectinload(Quiz.questions)
                .selectinload(Question.answers)
            )
            .where(Quiz.id == quiz.id)
        )

        quiz = result.scalar_one()

        correct = 0
        total = len(quiz.questions)

        attempt = QuizAttempt(
            user_id=user.id,
            company_id=quiz.company_id,
            quiz_id=quiz.id,
            correct_answers=0,
            total_questions=total
        )

        db.add(attempt)
        await db.flush()

        for answer_data in answers:
            question = next(
                q for q in quiz.questions
                if q.id == answer_data.question_id
            )

            correct_ids = {int(a.id) for a in question.answers if a.is_correct}
            selected_ids = {int(x) for x in answer_data.answer_ids}

            is_correct = correct_ids == selected_ids

            if is_correct:
                correct += 1

            for answer_id in selected_ids:
                db.add(
                    UserAnswer(
                        attempt_id=attempt.id,
                        question_id=question.id,
                        answer_id=answer_id,
                        is_correct=is_correct
                    )
                )

                await RedisQuizService.save_answer(
                    user_id=user.id,
                    company_id=quiz.company_id,
                    quiz_id=quiz.id,
                    question_id=question.id,
                    answer_id=answer_id,
                    is_correct=is_correct,
                )

        attempt.correct_answers = correct

        user.last_quiz_attempt_at = datetime.datetime.now()
        db.add(user)

        await db.flush()
        await db.commit()
        await db.refresh(attempt)

        return {
            "correct_answers": correct,
            "total_questions": total,
            "score": round(correct / total * 100, 2) if total else 0
        }

    @staticmethod
    async def get_company_average(
        db,
        user_id,
        company_id
    ):
        result = await db.execute(
            select(QuizAttempt)
            .where(
                QuizAttempt.user_id == user_id,
                QuizAttempt.company_id == company_id
            )
        )

        attempts = result.scalars().all()

        if not attempts:
            return 0

        scores = [
            (a.correct_answers / a.total_questions) * 100
            for a in attempts
        ]

        return round(sum(scores) / len(scores), 2)


    @staticmethod
    async def get_global_average(
        db,
        user_id
    ):
        result = await db.execute(
            select(
                func.sum(
                    QuizAttempt.correct_answers
                ),
                func.sum(
                    QuizAttempt.total_questions
                )
            ).where(
                QuizAttempt.user_id == user_id
            )
        )

        correct, total = result.one()

        if not total:
            return 0

        return round(
            correct / total * 100,
            2
        )
