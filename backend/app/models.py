from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.sql import func
import enum
from app.database import Base  # Добавляем импорт Base

class UserRole(enum.Enum):
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    vk_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    first_name = Column(String)
    last_name = Column(String)
    photo_url = Column(String, nullable=True)
    access_token = Column(String)
    refresh_token = Column(String, nullable=True)
    token_expires = Column(DateTime(timezone=True), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.GUEST)
    is_active = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)  # Поле для подтверждения пользователя
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())