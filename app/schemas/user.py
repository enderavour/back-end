from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    username: str


class SignUpRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    username: str | None = None


class UserDetailResponse(UserSchema):
    pass


class UsersListResponse(BaseModel):
    users: list[UserSchema]
