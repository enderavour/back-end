import csv
import io
from app.services.redis_service import RedisQuizService

class ExportService:
    @staticmethod
    async def export_user_json(user_id: int):
        return await RedisQuizService.get_user_answers(user_id)

    @staticmethod
    async def export_company_json(company_id: int):
        return await RedisQuizService.get_company_answers(company_id)


    @staticmethod
    async def export_quiz_json(company_id: int, quiz_id: int):
        return await RedisQuizService.get_quiz_answers(company_id, quiz_id)

    @staticmethod
    def _to_csv(data):
        buffer = io.StringIO()

        writer = csv.writer(buffer)

        writer.writerow([
            "user_id",
            "company_id",
            "quiz_id",
            "question_id",
            "answer_id",
            "is_correct"
        ])

        for item in data:
            writer.writerow([
                item["user_id"],
                item["company_id"],
                item["quiz_id"],
                item["question_id"],
                item["answer_id"],
                item["is_correct"]
            ])

        return buffer.getvalue()

    @staticmethod
    async def export_quiz_csv(company_id: int, quiz_id: int):
        data = await RedisQuizService.get_quiz_answers(
            company_id,
            quiz_id
        )

        return ExportService._to_csv(data)

    @staticmethod
    async def export_company_csv(company_id):
        return ExportService._to_csv(await RedisQuizService.get_company_answers(company_id))

    @staticmethod
    async def export_user_csv(user_id: int):
        return ExportService._to_csv(await RedisQuizService.get_user_answers(user_id))

    @staticmethod
    async def export_company_user_json(company_id: int, user_id: int):
        return await RedisQuizService.get_company_user_answers(company_id, user_id)


    @staticmethod
    async def export_company_user_csv(company_id: int, user_id: int):
        data = await RedisQuizService.get_company_user_answers(company_id, user_id)
        return ExportService._to_csv(data)
