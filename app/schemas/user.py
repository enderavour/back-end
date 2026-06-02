from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)


class SignUpRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    username: str | None = None
    password: str | None = None


class UserDetailResponse(UserSchema):
    pass


class UsersListResponse(BaseModel):
    users: list[UserSchema]
