from fastapi import HTTPException, status

from app.services.user import UserService
from app.core.security import verify_password, create_access_token
from app.schemas.auth import TokenResponseDTO


class AuthService:
    @staticmethod
    async def signin(db, data):
        user = await UserService.get_user_by_email(db, data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token = create_access_token({"sub": str(user.id)})

        return TokenResponseDTO(
            access_token=token,
            token_type="bearer"
        )
