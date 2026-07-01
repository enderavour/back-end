import pytest
from app.services.redis_service import RedisQuizService
from app.services.export import ExportService

@pytest.mark.asyncio
async def test_export_user_json():
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=True
    )

    data = await ExportService.export_user_json(1)

    assert len(data) == 1
    assert data[0]["user_id"] == 1


@pytest.mark.asyncio
async def test_export_company_json():
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=10,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=True
    )

    await RedisQuizService.save_answer(
        user_id=2,
        company_id=20,
        quiz_id=2,
        question_id=2,
        answer_id=2,
        is_correct=False
    )

    data = await ExportService.export_company_json(10)

    assert len(data) == 1
    assert data[0]["company_id"] == 10



@pytest.mark.asyncio
async def test_export_company_user_json():
    await RedisQuizService.save_answer(
        user_id=5,
        company_id=10,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=True
    )

    await RedisQuizService.save_answer(
        user_id=6,
        company_id=10,
        quiz_id=1,
        question_id=1,
        answer_id=2,
        is_correct=False
    )

    data = await ExportService.export_company_user_json(
        10,
        5
    )

    assert len(data) == 1
    assert data[0]["user_id"] == 5


@pytest.mark.asyncio
async def test_export_quiz_json():
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=100,
        question_id=1,
        answer_id=1,
        is_correct=True
    )

    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=200,
        question_id=1,
        answer_id=1,
        is_correct=True
    )

    data = await ExportService.export_quiz_json(
        1,
        100
    )

    assert len(data) == 1
    assert data[0]["quiz_id"] == 100


def test_to_csv():
    data = [
        {
            "user_id": 1,
            "company_id": 2,
            "quiz_id": 3,
            "question_id": 4,
            "answer_id": 5,
            "is_correct": True,
        }
    ]

    csv = ExportService._to_csv(data)

    assert "user_id" in csv
    assert "company_id" in csv
    assert "quiz_id" in csv
    assert "1,2,3,4,5,True" in csv


@pytest.mark.asyncio
async def test_export_user_csv():
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=True
    )

    csv_data = await ExportService.export_user_csv(1)

    assert "user_id" in csv_data
    assert "1,1,1,1,1,True" in csv_data
