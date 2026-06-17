import pytest
from app.services.redis_service import RedisQuizService
from app.services.analytics_service import AnalyticsService

@pytest.mark.asyncio
async def test_get_user_stats():
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=True,
    )

    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=2,
        answer_id=2,
        is_correct=False,
    )

    stats = await AnalyticsService.get_user_stats(1)

    assert stats["total_answers"] == 2
    assert stats["correct_answers"] == 1
    assert stats["rating"] == 50


@pytest.mark.asyncio
async def test_get_user_quiz_stats():
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=True,
    )

    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=2,
        answer_id=2,
        is_correct=False,
    )

    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=2,
        question_id=1,
        answer_id=1,
        is_correct=True,
    )

    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=2,
        question_id=2,
        answer_id=2,
        is_correct=True,
    )

    stats = await AnalyticsService.get_user_quiz_stats(1)

    assert len(stats) == 2

    assert stats[1]["score"] == 50
    assert stats[2]["score"] == 100

    assert "from" in stats[1]
    assert "to" in stats[1]

    assert stats[1]["from"] <= stats[1]["to"]


@pytest.mark.asyncio
async def test_get_user_last_attempts():
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=True,
    )

    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=2,
        question_id=1,
        answer_id=1,
        is_correct=False,
    )

    stats = await AnalyticsService.get_user_last_attempts(1)

    assert len(stats) == 2

    assert 1 in stats
    assert 2 in stats


@pytest.mark.asyncio
async def test_company_stats():
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=True,
    )

    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=2,
        answer_id=2,
        is_correct=False,
    )

    await RedisQuizService.save_answer(
        user_id=2,
        company_id=1,
        quiz_id=2,
        question_id=1,
        answer_id=1,
        is_correct=True,
    )

    await RedisQuizService.save_answer(
        user_id=2,
        company_id=1,
        quiz_id=2,
        question_id=2,
        answer_id=2,
        is_correct=False,
    )

    stats = await AnalyticsService.get_company_stats(1)

    assert len(stats) == 1

    week = next(iter(stats.values()))

    assert week["rating"] == 50


@pytest.mark.asyncio
async def test_company_user_stats():
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=False,
    )

    await RedisQuizService.save_answer(
        user_id=2,
        company_id=1,
        quiz_id=1,
        question_id=2,
        answer_id=2,
        is_correct=True,
    )

    stats = await AnalyticsService.get_company_user_stats(1)

    assert len(stats) == 2

    assert stats[1]["score"] == 0
    assert stats[2]["score"] == 100


@pytest.mark.asyncio
async def test_company_last_activity():
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=True,
    )

    await RedisQuizService.save_answer(
        user_id=2,
        company_id=1,
        quiz_id=1,
        question_id=2,
        answer_id=2,
        is_correct=False,
    )

    stats = await AnalyticsService.get_company_last_activity(1)

    assert len(stats) == 2

    assert 1 in stats
    assert 2 in stats
