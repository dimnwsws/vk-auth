from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import User, UserRole
from app.schemas import User as UserSchema
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


# Функция для проверки прав администратора
async def check_admin_rights(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    admin_roles = [UserRole.SITE_SUPPORT, UserRole.SITE_DEVELOPER, UserRole.SITE_FOUNDER]

    if current_user.role not in admin_roles:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return current_user


# Получение списка всех пользователей
@router.get("/users", response_model=List[UserSchema])
async def get_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(check_admin_rights)
):
    users = db.query(User).offset(skip).limit(limit).all()

    # Преобразуем данные для ответа
    result = []
    for user in users:
        user_dict = {
            "id": user.id,
            "vk_id": user.vk_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "photo_url": user.photo_url,
            "email": user.email,
            "role": user.role.name if user.role else "GUEST",  # Используем имя enum
            "is_approved": user.is_approved,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
        result.append(user_dict)

    return result


# Получение информации о конкретном пользователе
@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(check_admin_rights)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Подготавливаем данные для ответа
    user_dict = {
        "id": db_user.id,
        "vk_id": db_user.vk_id,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "photo_url": db_user.photo_url,
        "email": db_user.email,
        "role": db_user.role.name if db_user.role else "GUEST",  # Используем имя enum
        "is_approved": db_user.is_approved,
        "is_active": db_user.is_active,
        "created_at": db_user.created_at,
        "updated_at": db_user.updated_at
    }

    return user_dict


# Подтверждение пользователя
@router.put("/users/{user_id}/approve", response_model=UserSchema)
async def approve_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(check_admin_rights)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.is_approved = True
    db.commit()
    db.refresh(db_user)

    # Подготавливаем данные для ответа
    user_dict = {
        "id": db_user.id,
        "vk_id": db_user.vk_id,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "photo_url": db_user.photo_url,
        "email": db_user.email,
        "role": db_user.role.name if db_user.role else "GUEST",  # Используем имя enum
        "is_approved": db_user.is_approved,
        "is_active": db_user.is_active,
        "created_at": db_user.created_at,
        "updated_at": db_user.updated_at
    }

    return user_dict


# Обновление роли пользователя
@router.put("/users/{user_id}/role", response_model=UserSchema)
async def update_user_role(
        user_id: int,
        role: str = Body(..., embed=True),
        db: Session = Depends(get_db),
        current_user: User = Depends(check_admin_rights)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Проверяем, существует ли такая роль
    try:
        user_role = UserRole[role]  # Используем имена перечислений (GUEST, USER, etc.)
        db_user.role = user_role
        db.commit()
        db.refresh(db_user)

        # Подготавливаем данные для ответа
        user_dict = {
            "id": db_user.id,
            "vk_id": db_user.vk_id,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name,
            "photo_url": db_user.photo_url,
            "email": db_user.email,
            "role": db_user.role.name if db_user.role else "GUEST",  # Используем имя enum
            "is_approved": db_user.is_approved,
            "is_active": db_user.is_active,
            "created_at": db_user.created_at,
            "updated_at": db_user.updated_at
        }

        return user_dict
    except (KeyError, ValueError):
        raise HTTPException(status_code=400, detail=f"Invalid role: {role}")


# Удаление пользователя
@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(check_admin_rights)
):
    # Нельзя удалить самого себя
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return None