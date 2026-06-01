from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth0 import verify_auth0_token, decode_auth0_token
from app.db.deps import get_db

from app.services.user import UserService
from app.schemas.user import SignUpRequest


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload

    except JWTError:
        raise ValueError("Invalid token")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({"exp": expire})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    payload = decode_token(token)

    user_id = payload.get("sub")

    user = await UserService.get_user_by_id(db, int(user_id))

    if not user:
        raise HTTPException(status_code=401)

    return user


async def get_auth_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    payload = decode_auth0_token(token)

    print(payload)

    email = payload.get("email")

    if not email:
        raise HTTPException(status_code=401, detail="Invalid Auth0 token")

    user = await UserService.get_user_by_email(db, email)

    if not user:
        user = await UserService.create_user(
            db,
            SignUpRequest(
                email=email,
                username=email.split("@")[0],
                password="auth0-user"
            )
        )

    return user

async def get_auth0_user(token: str = Depends(oauth2_scheme)):
    return verify_auth0_token(token)
