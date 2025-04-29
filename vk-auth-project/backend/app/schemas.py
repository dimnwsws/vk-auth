# Обновленный schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum


class UserRoleEnum(str, Enum):
    GUEST = "GUEST"
    USER = "USER"
    ORG_DEPUTY = "ORG_DEPUTY"
    ORG_LEADER = "ORG_LEADER"
    ADMIN_OBSERVER = "ADMIN_OBSERVER"
    CHIEF_OBSERVER_DEPUTY = "CHIEF_OBSERVER_DEPUTY"
    CHIEF_OBSERVER = "CHIEF_OBSERVER"
    CURATOR = "CURATOR"
    CHIEF_ADMIN_DEPUTY = "CHIEF_ADMIN_DEPUTY"
    CHIEF_ADMIN = "CHIEF_ADMIN"
    SITE_SUPPORT = "SITE_SUPPORT"
    SITE_DEVELOPER = "SITE_DEVELOPER"
    SITE_FOUNDER = "SITE_FOUNDER"


class UserBase(BaseModel):
    vk_id: str
    first_name: str
    last_name: str
    photo_url: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRoleEnum] = UserRoleEnum.GUEST
    is_approved: Optional[bool] = False


class UserCreate(UserBase):
    access_token: str
    refresh_token: Optional[str] = None
    token_expires: Optional[datetime] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    vk_id: Optional[str] = None


class ErrorResponse(BaseModel):
    detail: str


class SuccessResponse(BaseModel):
    message: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: User