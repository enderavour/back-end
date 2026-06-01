from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.schemas.user import SignInRequest, SignUpRequest
from app.services.user import UserService
from app.core.security import (
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/signin")
async def signin(
    data: SignInRequest,
    db: AsyncSession = Depends(get_db)
):
    user = await UserService.get_user_by_email(
        db,
        data.email
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/signup")
async def signup(data: SignUpRequest, db: AsyncSession = Depends(get_db)):
    return await UserService.create_user(db, data)
