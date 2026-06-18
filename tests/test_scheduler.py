import pytest
import uuid
from datetime import datetime, timedelta
from app.services.user import UserService
from app.schemas.user import SignUpRequest
from app.services.company import CompanyService
from app.schemas.company import CompanyCreate
from app.models.company_member import CompanyMember
from app.schemas.quiz import (
    QuizCreate,
    QuestionCreate,
    AnswerOptionCreate,
)
from app.services.quiz import QuizService
from app.services.scheduler_service import SchedulerService
from app.services.notification import NotificationService
from app.models.quiz_attempt import QuizAttempt

# A function for creating the quiz without duplicating the code in tests
async def create_test_quiz(db_session, company):
    quiz_data = QuizCreate(
        title="Python Quiz",
        description="Test quiz",
        questions=[
            QuestionCreate(
                title="Question 1",
                answers=[
                    AnswerOptionCreate(
                        title="Correct",
                        is_correct=True
                    ),
                    AnswerOptionCreate(
                        title="Wrong",
                        is_correct=False
                    ),
                ],
            ),
            QuestionCreate(
                title="Question 2",
                answers=[
                    AnswerOptionCreate(
                        title="Correct",
                        is_correct=True
                    ),
                    AnswerOptionCreate(
                        title="Wrong",
                        is_correct=False
                    ),
                ],
            ),
        ],
    )

    return await QuizService.create_quiz(
        db_session,
        company.id,
        quiz_data,
    )


 # 1 test
@pytest.mark.asyncio
async def test_notification_if_no_attempt(db_session):
    unique_email = f"{uuid.uuid4()}@test.com"
    unique_username = f"user_{uuid.uuid4().hex[:8]}"

    user = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=unique_email,
            username=unique_username,
            password="123456"
        )
    )

    company = await CompanyService.create_company(
        db_session,
        data=CompanyCreate(name="Test", description="desc"),
        owner_id=user.id
    )

    member = CompanyMember(
        company_id=company.id,
        user_id=user.id,
        role="owner"
    )

    db_session.add(member)
    await db_session.flush()

    await create_test_quiz(db_session, company)

    await SchedulerService.check_quizzes(db_session)

    notifications = await NotificationService.get_user_notifications(
        db_session,
        user.id
    )

    assert len(notifications) == 1

#2 test
@pytest.mark.asyncio
async def test_no_notification_if_recent_attempt(db_session):
    unique_email = f"{uuid.uuid4()}@test.com"
    unique_username = f"user_{uuid.uuid4().hex[:8]}"

    user = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=unique_email,
            username=unique_username,
            password="123456"
        )
    )

    company = await CompanyService.create_company(
        db_session,
        data=CompanyCreate(name="Test", description="desc"),
        owner_id=user.id
    )

    member = CompanyMember(
        company_id=company.id,
        user_id=user.id,
        role="owner"
    )

    quiz = await create_test_quiz(db_session, company)

    attempt = QuizAttempt(
        user_id=user.id,
        company_id=company.id,
        quiz_id=quiz.id,
        correct_answers=2,
        total_questions=2,
        created_at=datetime.utcnow(),
    )

    db_session.add(attempt)
    await db_session.commit()

    await SchedulerService.check_quizzes(db_session)

    notifications = await NotificationService.get_user_notifications(
        db_session,
        user.id,
    )

    reminders = [
        n for n in notifications
        if "Please complete quiz" in n.message
    ]

    assert len(reminders) == 0
