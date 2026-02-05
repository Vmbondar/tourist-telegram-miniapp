from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    telegram_id: Optional[int] = None
    telegram_username: Optional[str] = None


class UserCreate(UserBase):
    password: Optional[str] = Field(None, min_length=8)


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TelegramAuth(BaseModel):
    init_data: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str
