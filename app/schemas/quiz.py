from pydantic import BaseModel

class AnswerOptionCreate(BaseModel):
    title: str
    is_correct: bool


class QuestionCreate(BaseModel):
    title: str
    answers: list[AnswerOptionCreate]


class QuizCreate(BaseModel):
    title: str
    description: str | None = None
    questions: list[QuestionCreate]
