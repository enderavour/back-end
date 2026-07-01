from pydantic import BaseModel

class QuestionAnswerRequest(BaseModel):
    question_id: int
    answer_ids: list[int]

class QuizSubmitRequest(BaseModel):
    answers: list[QuestionAnswerRequest]
