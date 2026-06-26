from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.schemas.user import SignInRequest, SignUpRequest
from app.services.user import UserService
from app.core.security import (
    verify_password,
    create_access_token
)
from app.services.auth import AuthService
from app.schemas.auth import TokenResponseDTO

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/signin", response_model=TokenResponseDTO)
async def signin(
    data: SignInRequest,
    db: AsyncSession = Depends(get_db)
):
    return await AuthService.signin(db, data)


@router.post("/signup")
async def signup(data: SignUpRequest, db: AsyncSession = Depends(get_db)):
    return await UserService.create_user(db, data)
