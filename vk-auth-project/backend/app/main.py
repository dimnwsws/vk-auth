from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.database import engine, Base
from app.models import UserRole  # Добавим импорт UserRole
from app.routers import auth, users, admin, google_sheets  # Добавляем импорт google_sheets
from app.config import get_settings

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

# Задаем значения по умолчанию для существующих записей
try:
    with engine.begin() as conn:
        # Обновляем существующие записи с NULL значениями
        # Используем UserRole.GUEST.name вместо строки 'Гость'
        conn.execute(
            text(f"UPDATE users SET role = '{UserRole.GUEST.name}' WHERE role IS NULL")
        )
        conn.execute(
            text("UPDATE users SET is_approved = 0 WHERE is_approved IS NULL")
        )
except Exception as e:
    print(f"Ошибка при обновлении данных: {e}")

# Инициализируем FastAPI приложение
app = FastAPI(
    title="VK Auth API",
    description="API для авторизации через ВКонтакте",
    version="1.0.0"
)

# Получаем настройки
settings = get_settings()

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(google_sheets.router, prefix="/api")
# Корневой маршрут
@app.get("/")
async def root():
    return {"message": "Добро пожаловать в VK Auth API"}

# Проверка здоровья
@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})