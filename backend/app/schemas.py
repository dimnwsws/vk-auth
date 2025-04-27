from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

from app.models import UserRole



class UserRoleEnum(str, Enum):
    GUEST = "Гость"
    USER = "Пользователь"
    ORG_DEPUTY = "Заместитель организации"
    ORG_LEADER = "Лидер организации"
    ADMIN_OBSERVER = "Следящая администрация"
    CHIEF_OBSERVER_DEPUTY = "Заместитель Главного Следящего"
    CHIEF_OBSERVER = "Главный Следящий"
    CURATOR = "Куратор"
    CHIEF_ADMIN_DEPUTY = "Заместитель Главного администратора"
    CHIEF_ADMIN = "Главный администратор"
    SITE_SUPPORT = "Поддержка Сайта"
    SITE_DEVELOPER = "Разработчик Сайта"
    SITE_FOUNDER = "Основатель Сайта"


class UserBase(BaseModel):
    vk_id: str
    first_name: str
    last_name: str
    photo_url: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = UserRole.GUEST
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
        from_attributes = True  # Использовать вместо orm_mode
        # Указываем, что модель должна обрабатывать типы данных из ORM
        json_encoders = {
            UserRole: lambda v: v.name
        }


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