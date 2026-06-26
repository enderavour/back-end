from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import SignUpRequest, UserUpdateRequest
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, data: SignUpRequest):
        try:
            logger.info(f"Creating user with email={data.email}")

            user_dto = UserDTO(
                email=data.email,
                username=data.username,
                password=hash_password(data.password)
            )

            created_user = await UserRepository.create(db, user_dto)

            logger.info(f"User created with id={created_user.id}")

            return created_user

        except SQLAlchemyError as e:
            logger.error(f"Database error while creating user: {e}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            )

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        logger.info(f"Fetching user with id={user_id}")

        user = await UserRepository.get_by_id(db, user_id)

        if not user:
            logger.warning(f"User with id={user_id} not found")

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found",
            )

        return user

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, data: UserUpdateRequest):
        user = await UserRepository.get_by_id(db, user_id)

        if not user:
            logger.warning(f"User {user_id} not found")

            raise HTTPException(status_code=404, detail="User Not Found")

        update_data = data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])

        updated_user = await UserRepository.update(db, user, update_data)

        logger.info(f"User {user_id} updated")
        return updated_user

    @staticmethod
    async def get_users(db, skip, limit=10):
        return await UserRepository.get_all(db, skip, limit)

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int):
        logger.info(f"Deleting user with id={user_id}")

        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            logger.error(f"User with id={user_id} not found")

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        await UserRepository.delete(db, user)

        logger.info(f"User with id={user_id} deleted")

        return {"message": "User deleted successfully"}

    @staticmethod
    async def get_user_by_id(
        db: AsyncSession,
        user_id: int,
    ):
        result = await UserRepository.get_by_id(db, user_id)
        return result

    @staticmethod
    async def get_user_by_email(
        db: AsyncSession,
        email: str
    ):
        result = await UserRepository.get_by_email(db, email)
        return result


    @staticmethod
    async def get_or_create_auth0_user(db: AsyncSession, email: str):
        user = await UserService.get_user_by_email(db, email)

        if user:
            return user

        user = {
            "email": email,
            "username": email.split("@")[0],
            "password": ""
        }

        return await UserRepository.create_from_dict(db, user)
