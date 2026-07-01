import pytest
from app.services.redis_service import RedisQuizService

@pytest.mark.asyncio
async def test_save_answer(
    redis_client
):
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=True,
    )

    data = await RedisQuizService.get_answer(
        1,
        1,
        1,
        1
    )

    assert data is not None
    assert data["user_id"] == 1
    assert data["is_correct"] is True


@pytest.mark.asyncio
async def test_answer_has_ttl(
    redis_client
):
    await RedisQuizService.save_answer(
        user_id=1,
        company_id=1,
        quiz_id=1,
        question_id=1,
        answer_id=1,
        is_correct=True,
    )

    ttl = await redis_client.ttl(
        "quiz_answer:1:1:1:1"
    )

    assert ttl > 0


@pytest.mark.asyncio
async def test_delete_answer(
    redis_client
):
    key = "quiz_answer:1:1:1"

    await redis_client.set(
        key,
        "test"
    )

    await redis_client.delete(key)

    value = await redis_client.get(key)

    assert value is None
