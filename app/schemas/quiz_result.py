from pydantic import BaseModel

class QuizResultResponse(BaseModel):
    correct_answers: int
    total_questions: int
    score: float
