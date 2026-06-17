from app.services.redis_service import RedisQuizService
from collections import defaultdict
import datetime

class AnalyticsService:
    @staticmethod
    async def get_user_stats(user_id: int):
        answers = await RedisQuizService.get_user_answers(user_id)

        total = len(answers)
        correct = sum(1 for a in answers if a["is_correct"])

        return {
            "total_answers": total,
            "correct_answers": correct,
            "rating": round(correct / total * 100, 2) if total else 0
        }

    @staticmethod
    async def get_user_quiz_stats(user_id: int):
        answers = await RedisQuizService.get_user_answers(user_id)

        quizzes = defaultdict(lambda: {
            "correct": 0,
            "total": 0,
            "first": None,
            "last": None,
        })

        for answer in answers:
            quiz = quizzes[answer["quiz_id"]]

            quiz["total"] += 1

            if answer["is_correct"]:
                quiz["correct"] += 1

            ts = datetime.datetime.fromtimestamp(answer["timestamp"])

            if quiz["first"] is None or ts < quiz["first"]:
                quiz["first"] = ts

            if quiz["last"] is None or ts > quiz["last"]:
                quiz["last"] = ts

        return {
            quiz_id: {
                "score": round(v["correct"] / v["total"] * 100, 2),
                "from": v["first"].isoformat(),
                "to": v["last"].isoformat()
            }
            for quiz_id, v in quizzes.items()
        }

    @staticmethod
    async def get_user_last_attempts(user_id: int):
        answers = await RedisQuizService.get_user_answers(user_id)

        last = {}

        for a in answers:
            qid = a["quiz_id"]
            last[qid] = max(last.get(qid, 0), a.get("timestamp", 0))

        return last

    @staticmethod
    async def get_company_stats(company_id: int):
        answers = await RedisQuizService.get_company_answers(company_id)

        weeks = defaultdict(lambda: {
            "correct": 0,
            "total": 0
        })

        for answer in answers:
            dt = datetime.datetime.fromtimestamp(answer["timestamp"])

            week = dt.strftime("%Y-W%U")

            weeks[week]["total"] += 1

            if answer["is_correct"]:
                weeks[week]["correct"] += 1

        return {
            week: {
                "rating": round(
                    data["correct"] / data["total"] * 100,
                    2
                )
            }
            for week, data in weeks.items()
        }


    @staticmethod
    async def get_company_user_stats(company_id: int):
        answers = await RedisQuizService.get_company_answers(company_id)

        users = defaultdict(lambda: {"correct": 0, "total": 0})

        for a in answers:
            u = users[a["user_id"]]
            u["total"] += 1
            if a["is_correct"]:
                u["correct"] += 1

        return {
            user_id: {
                "score": round(v["correct"] / v["total"] * 100, 2)
            }
            for user_id, v in users.items()
        }

    @staticmethod
    async def get_company_last_activity(company_id: int):
        answers = await RedisQuizService.get_company_answers(company_id)

        last = {}

        for a in answers:
            uid = a["user_id"]
            last[uid] = max(last.get(uid, 0), a.get("timestamp", 0))

        return last


    @staticmethod
    async def get_company_user_quiz_stats(
        company_id: int,
        user_id: int
    ):
        answers = await RedisQuizService.get_company_user_answers(
            company_id,
            user_id
        )

        quizzes = defaultdict(lambda: {
            "correct": 0,
            "total": 0,
            "first": None,
            "last": None,
        })

        for answer in answers:
            quiz = quizzes[answer["quiz_id"]]

            quiz["total"] += 1

            if answer["is_correct"]:
                quiz["correct"] += 1

            ts = datetime.datetime.fromtimestamp(answer["timestamp"])

            if quiz["first"] is None or ts < quiz["first"]:
                quiz["first"] = ts

            if quiz["last"] is None or ts > quiz["last"]:
                quiz["last"] = ts

        return {
            quiz_id: {
                "score": round(
                    data["correct"] / data["total"] * 100,
                    2
                ),
                "from": data["first"].isoformat(),
                "to": data["last"].isoformat()
            }
            for quiz_id, data in quizzes.items()
        }
