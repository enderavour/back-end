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
from app.schemas.quiz_submit import QuestionAnswerRequest
from app.models.quiz import AnswerOption, Quiz, Question
from app.models.company import Company
from sqlalchemy import select
from app.models.quiz_attempt import QuizAttempt
from app.models.user_answer import UserAnswer

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


@pytest.mark.asyncio
async def test_take_quiz(db_session):
    user = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    company = Company(
        name="Test Company",
        owner_id=user.id
    )

    db_session.add(company)
    await db_session.flush()

    quiz = Quiz(
        title="Python Quiz",
        description="Test quiz",
        company_id=company.id
    )

    db_session.add(quiz)
    await db_session.flush()

    question = Question(
        title="What is Python?",
        quiz_id=quiz.id
    )

    db_session.add(question)
    await db_session.flush()

    correct_answer = AnswerOption(
        title="Programming language",
        question_id=question.id,
        is_correct=True
    )

    wrong_answer = AnswerOption(
        title="Database",
        question_id=question.id,
        is_correct=False
    )

    db_session.add_all([correct_answer, wrong_answer])
    await db_session.flush()

    result = await QuizService.take_quiz(
        db_session,
        quiz,
        user,
        [
            QuestionAnswerRequest(
                question_id=question.id,
                answer_ids=[correct_answer.id]
            )
        ]
    )

    assert result["correct_answers"] == 1
    assert result["total_questions"] == 1
    assert result["score"] == 100


@pytest.mark.asyncio
async def test_user_answers_saved(db_session):
    user = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    company = Company(name="Test Company", owner_id=user.id)
    db_session.add(company)
    await db_session.flush()

    quiz = Quiz(
        title="Python Quiz",
        description="Test quiz",
        company_id=company.id
    )
    db_session.add(quiz)
    await db_session.flush()

    question = Question(
        title="What is Python?",
        quiz_id=quiz.id
    )
    db_session.add(question)
    await db_session.flush()

    answer = AnswerOption(
        title="Programming language",
        question_id=question.id,
        is_correct=True
    )
    db_session.add(answer)
    await db_session.flush()

    answers = [
        QuestionAnswerRequest(
            question_id=question.id,
            answer_ids=[answer.id]
        )
    ]

    await QuizService.take_quiz(
        db_session,
        quiz,
        user,
        answers
    )

    result = await db_session.execute(select(UserAnswer))
    user_answers = result.scalars().all()

    assert len(user_answers) > 0

@pytest.mark.asyncio
async def test_company_average(db_session):
    user = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    company = Company(name="Test Company", owner_id=user.id)
    db_session.add(company)
    await db_session.flush()

    quiz = Quiz(
        title="Quiz",
        description="Test",
        company_id=company.id
    )
    db_session.add(quiz)
    await db_session.flush()

    attempt = QuizAttempt(
        user_id=user.id,
        company_id=company.id,
        quiz_id=quiz.id,
        correct_answers=1,
        total_questions=1
    )
    db_session.add(attempt)

    attempt2 = QuizAttempt(
        user_id=user.id,
        company_id=company.id,
        quiz_id=quiz.id,
        correct_answers=1,
        total_questions=2
    )
    db_session.add(attempt2)

    await db_session.flush()

    average = await QuizService.get_company_average(
        db_session,
        user.id,
        company.id
    )

    assert average == 75

@pytest.mark.asyncio
async def test_last_attempt_updated(
    db_session
):
    user = await UserService.create_user(
        db_session,
        SignUpRequest(
            email=f"{uuid.uuid4()}@test.com",
            username=f"user_{uuid.uuid4().hex[:8]}",
            password="123456"
        )
    )

    company = Company(
        name="Test Company",
        owner_id=user.id
    )
    db_session.add(company)
    await db_session.flush()

    quiz = Quiz(
        title="Python Quiz",
        description="Test quiz",
        company_id=company.id
    )
    db_session.add(quiz)
    await db_session.flush()

    question = Question(
        title="What is Python?",
        quiz_id=quiz.id
    )
    db_session.add(question)
    await db_session.flush()

    answer = AnswerOption(
        title="Programming language",
        question_id=question.id,
        is_correct=True
    )
    db_session.add(answer)
    await db_session.flush()

    answers = [
        QuestionAnswerRequest(
            question_id=question.id,
            answer_ids=[answer.id]
        )
    ]

    assert user.last_quiz_attempt_at is None

    await QuizService.take_quiz(
        db_session,
        quiz,
        user,
        answers
    )

    await db_session.refresh(user)

    assert user.last_quiz_attempt_at is not None
