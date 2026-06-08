from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.services.quiz import QuizService
from app.core.security import get_auth_user
from app.schemas.quiz import QuizCreate


router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"]
)

@router.post(
    "/companies/{company_id}"
)
async def create_quiz(
    company_id: int,
    data: QuizCreate,
    current_user=Depends(get_auth_user),
    db: AsyncSession = Depends(get_db)
):
    return await QuizService.create_quiz(
        db,
        company_id,
        data
    )



@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await QuizService.get_quiz(
        db,
        quiz_id
    )


@router.get("/company/{company_id}")
async def get_company_quizzes(
    company_id: int,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    return await QuizService.get_company_quizzes(
        db,
        company_id,
        skip,
        limit
    )


@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: int,
    current_user = Depends(get_auth_user),
    db: AsyncSession = Depends(get_db)
):
    quiz = await QuizService.get_quiz(db, quiz_id)

    if not quiz:
        raise HTTPException(404, "Quiz not found")

    await QuizService.delete_quiz(db, quiz)

    return {"message": "Quiz deleted"}
