import json

from app.core.redis import get_redis

class RedisQuizService:
    @staticmethod
    async def save_answer(
        user_id: int,
        company_id: int,
        quiz_id: int,
        question_id: int,
        answer_id: int,
        is_correct: bool
    ):
        key = f"quiz_answer:{user_id}:{quiz_id}:{question_id}:{answer_id}"

        data = {
            "user_id": user_id,
            "company_id": company_id,
            "quiz_id": quiz_id,
            "question_id": question_id,
            "answer_id": answer_id,
            "is_correct": is_correct
        }

        await get_redis().set(
            key,
            json.dumps(data),
            ex=60 * 60 * 48
        )

    @staticmethod
    async def get_answer(
        user_id: int,
        quiz_id: int,
        question_id: int,
        answer_id: int
    ):

        key = f"quiz_answer:{user_id}:{quiz_id}:{question_id}:{answer_id}"

        data = await get_redis().get(key)

        if not data:
            return None

        return json.loads(data)

    @staticmethod
    def _client():
        return get_redis()
