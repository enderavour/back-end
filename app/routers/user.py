from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.security import get_auth_user
from app.db.deps import get_db
from app.schemas.user import SignUpRequest, UserSchema, UserUpdateRequest
from app.services.user import UserService
from app.core.security import get_auth_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserSchema, status_code=201)
async def create_user(data: SignUpRequest, db: AsyncSession = Depends(get_db)):
    return await UserService.create_user(db, data)


@router.get("/")
async def get_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    return await UserService.get_users(db, skip, limit)


@router.get("/me", response_model=UserSchema)
async def me(
    current_user: UserSchema = Depends(get_auth_user),
):
    return current_user

@router.get("/auth0/me", response_model=UserSchema)
async def auth0_me(
    auth0_user=Depends(get_auth_user),
    db: AsyncSession = Depends(get_db),
):
    user = await UserService.get_or_create_auth0_user(
        db,
        auth0_user.email
    )

    return user

@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService.get_user(db, user_id)


@router.patch("/{user_id}")
async def update_user(
    user_id: int,
    data: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    return await UserService.update_user(db, user_id, data)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService.delete_user(db, user_id)
