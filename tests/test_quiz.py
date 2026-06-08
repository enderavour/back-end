import pytest
from app.schemas.quiz import (
    QuizCreate,
    QuestionCreate,
    AnswerOptionCreate,
)
from app.services.quiz import QuizService
from app.services.company import CompanyService
from app.services.user import UserService
from app.schemas.company import CompanyCreate
from app.schemas.user import SignUpRequest

from fastapi import HTTPException
import uuid

@pytest.mark.asyncio
async def test_create_quiz(db_session):
    owner = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    company = await CompanyService.create_company(
        db_session,
        CompanyCreate(
            name="Test Company",
            description="Test"
        ),
        owner.id
    )

    quiz_data = QuizCreate(
        title="Python Quiz",
        description="Test quiz",
        questions=[
            QuestionCreate(
                title="What is Python?",
                answers=[
                    AnswerOptionCreate(title="Programming language", is_correct=True),
                    AnswerOptionCreate(title="Database", is_correct=False),
                ],
            ),
            QuestionCreate(
                title="Which framework is for Python?",
                answers=[
                    AnswerOptionCreate(title="FastAPI", is_correct=True),
                    AnswerOptionCreate(title="PostgreSQL", is_correct=False),
                ],
            ),
        ],
    )

    quiz = await QuizService.create_quiz(
        db_session,
        company.id,
        quiz_data
    )

    assert quiz.id is not None
    assert quiz.title == "Python Quiz"


@pytest.mark.asyncio
async def test_quiz_requires_two_questions(db_session):
    owner = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    company = await CompanyService.create_company(
        db_session,
        CompanyCreate(name="Test Company"),
        owner.id
    )

    with pytest.raises(HTTPException):
        await QuizService.create_quiz(
            db_session,
            company.id,
            QuizCreate(
                title="Quiz",
                questions=[
                    QuestionCreate(
                        title="Question",
                        answers=[
                            AnswerOptionCreate(title="Answer", is_correct=True),
                            AnswerOptionCreate(title="Answer 2", is_correct=False),
                        ],
                    )
                ],
            ),
        )



@pytest.mark.asyncio
async def test_question_requires_two_answers(db_session):
    owner = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    company = await CompanyService.create_company(
        db_session,
        CompanyCreate(name="Test Company"),
        owner.id
    )

    invalid_quiz = QuizCreate(
        title="Invalid Quiz",
        questions=[
            QuestionCreate(
                title="Question 1",
                answers=[
                    AnswerOptionCreate(title="Only answer", is_correct=True),
                ],
            ),
            QuestionCreate(
                title="Question 2",
                answers=[
                    AnswerOptionCreate(title="A", is_correct=True),
                    AnswerOptionCreate(title="B", is_correct=False),
                ],
            ),
        ],
    )

    with pytest.raises(HTTPException):
        await QuizService.create_quiz(
            db_session,
            company.id,
            invalid_quiz
        )


@pytest.mark.asyncio
async def test_get_company_quizzes(db_session):
    owner = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    company = await CompanyService.create_company(
        db_session,
        CompanyCreate(name="Test Company"),
        owner.id
    )

    quizzes = await QuizService.get_company_quizzes(
        db_session,
        company.id
    )

    assert isinstance(quizzes, list)



@pytest.mark.asyncio
async def test_delete_quiz(db_session):
    owner = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    company = await CompanyService.create_company(
        db_session,
        CompanyCreate(name="Test Company"),
        owner.id
    )

    quiz_data = QuizCreate(
        title="Python Quiz",
        description="Test quiz",
        questions=[
            QuestionCreate(
                title="Question 1",
                answers=[
                    AnswerOptionCreate(title="Answer A", is_correct=True),
                    AnswerOptionCreate(title="Answer B", is_correct=False),
                ],
            ),
            QuestionCreate(
                title="Question 2",
                answers=[
                    AnswerOptionCreate(title="Answer A", is_correct=True),
                    AnswerOptionCreate(title="Answer B", is_correct=False),
                ],
            ),
        ],
    )

    quiz = await QuizService.create_quiz(
        db_session,
        company.id,
        quiz_data
    )

    await QuizService.delete_quiz(db_session, quiz)

    deleted = await QuizService.get_quiz(db_session, quiz.id)

    assert deleted is None
