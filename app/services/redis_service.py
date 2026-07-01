import json

from app.core.redis import get_redis
import time

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
            "is_correct": is_correct,
            "timestamp": time.time()
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

    @staticmethod
    async def get_user_answers(user_id: int):
        client = get_redis()

        keys = await client.keys(f"quiz_answer:{user_id}:*")

        result = []

        for key in keys:
            data = await client.get(key)

            if data:
                result.append(json.loads(data))

        return result

    @staticmethod
    async def get_company_answers(company_id: int):
        client = get_redis()

        keys = await client.keys("quiz_answer:*")

        result = []

        for key in keys:
            data = await client.get(key)

            if data:
                item = json.loads(data)

                if item["company_id"] == company_id:
                    result.append(item)

        return result

    @staticmethod
    async def get_quiz_answers(
        company_id: int,
        quiz_id: int
    ):
        answers = await RedisQuizService.get_company_answers(company_id)

        return [x for x in answers if x["quiz_id"] == quiz_id]

    @staticmethod
    async def get_company_user_answers(
        company_id: int,
        user_id: int
    ):
        answers = await RedisQuizService.get_company_answers(company_id)
        return [answer for answer in answers if answer["user_id"] == user_id]
