from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Cookie, Header
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
import httpx
import secrets
from urllib.parse import urlencode
from typing import Optional

from app.database import get_db
from app.models import User, UserRole
from app.schemas import Token, TokenData, UserCreate, User as UserSchema, AuthResponse
from app.config import get_settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

settings = get_settings()


# Создание JWT токена
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# Проверка JWT токена
async def verify_token(
        authorization: str = Header(None),
        token: str = Cookie(None)
):
    # Проверяем заголовок Authorization
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")

    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        vk_id: str = payload.get("sub")
        if vk_id is None:
            return None
        token_data = TokenData(vk_id=vk_id)
    except JWTError:
        return None
    return token_data


# Получение текущего пользователя
async def get_current_user(
        token_data: Optional[TokenData] = Depends(verify_token),
        db: Session = Depends(get_db)
):
    if not token_data:
        return None
    user = db.query(User).filter(User.vk_id == token_data.vk_id).first()
    return user


# Инициирование авторизации ВКонтакте
@router.get("/vk/login")
async def vk_login(request: Request):
    # Генерация state для защиты от CSRF
    state = secrets.token_urlsafe(16)

    # Параметры запроса авторизации ВК
    params = {
        "client_id": settings.VK_CLIENT_ID,
        "redirect_uri": settings.VK_REDIRECT_URI,
        "display": "page",
        "scope": "email",
        "response_type": "code",
        "state": state,
        "v": "5.131"
    }

    # Формирование URL для редиректа
    auth_url = f"https://oauth.vk.com/authorize?{urlencode(params)}"
    return {"auth_url": auth_url, "state": state}


# Обработка callback от ВКонтакте
@router.get("/vk/callback")
async def vk_callback(
        code: str = None,
        state: str = None,
        error: str = None,
        db: Session = Depends(get_db)
):
    print(f"Callback received with code: {code}, state: {state}, error: {error}")

    # Проверка на ошибки
    if error:
        print(f"Error in callback: {error}")
        return RedirectResponse(
            f"{settings.FRONTEND_URL}/auth-error?error={error}"
        )

    print("Getting access token from VK...")
    # Получение access token от ВК
    token_params = {
        "client_id": settings.VK_CLIENT_ID,
        "client_secret": settings.VK_CLIENT_SECRET,
        "redirect_uri": settings.VK_REDIRECT_URI,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        print(f"Sending request to VK for access token with params: {token_params}")
        token_response = await client.get(
            f"https://oauth.vk.com/access_token", params=token_params
        )

        print(f"VK token response status: {token_response.status_code}")
        token_data = token_response.json()
        print(f"Token data: {token_data}")

        if "error" in token_data:
            print(f"Error in token data: {token_data.get('error_description', 'Unknown error')}")
            return RedirectResponse(
                f"{settings.FRONTEND_URL}/auth-error?error={token_data.get('error_description', 'Unknown error')}"
            )

        print("Getting user data from VK API...")
        # Получение данных пользователя от ВК
        user_params = {
            "user_ids": token_data["user_id"],
            "fields": "photo_200",
            "access_token": token_data["access_token"],
            "v": "5.131",
        }

        print(f"Sending request to VK API with params: {user_params}")
        user_response = await client.get(
            "https://api.vk.com/method/users.get", params=user_params
        )

        print(f"VK API response status: {user_response.status_code}")
        user_data = user_response.json()
        print(f"User data: {user_data}")

        if "error" in user_data:
            print(f"Error in user data: {user_data['error']['error_msg']}")
            return RedirectResponse(
                f"{settings.FRONTEND_URL}/auth-error?error={user_data['error']['error_msg']}"
            )

        vk_user = user_data["response"][0]
        print(f"VK user: {vk_user}")

        # Проверка, существует ли пользователь в БД
        print(f"Checking if user exists in database with VK ID: {vk_user['id']}")
        db_user = db.query(User).filter(User.vk_id == str(vk_user["id"])).first()

        # Обновленная часть кода для создания пользователя
        if db_user:
            # Обновление данных пользователя
            db_user.first_name = vk_user["first_name"]
            db_user.last_name = vk_user["last_name"]
            db_user.photo_url = vk_user.get("photo_200", "")
            db_user.access_token = token_data["access_token"]
            if "email" in token_data:
                db_user.email = token_data["email"]
                print(f"Updated user email: {token_data['email']}")
        else:
            print(f"User not found, creating new user")
            # Создание нового пользователя
            user_create = UserCreate(
                vk_id=str(vk_user["id"]),
                first_name=vk_user["first_name"],
                last_name=vk_user["last_name"],
                photo_url=vk_user.get("photo_200", ""),
                access_token=token_data["access_token"],
                email=token_data.get("email")
            )
            # Создаем пользователя вручную с правильными полями enum
            db_user = User(
                vk_id=user_create.vk_id,
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                photo_url=user_create.photo_url,
                access_token=user_create.access_token,
                email=user_create.email,
                role=UserRole.GUEST,  # Используем правильное значение enum
                is_approved=False
            )
            db.add(db_user)

        print(f"Committing changes to database")
        db.commit()
        db.refresh(db_user)
        print(f"User data saved, ID: {db_user.id}")

        # Создание JWT токена
        print(f"Creating JWT token for user ID: {db_user.vk_id}")
        access_token = create_access_token(
            data={"sub": str(db_user.vk_id)},
        )
        print(f"JWT token created: {access_token[:10]}... (truncated)")

        # Перенаправление на фронтенд с токеном
        redirect_url = f"{settings.FRONTEND_URL}/auth-callback?token={access_token}&user_id={db_user.id}"
        print(f"Redirecting to frontend: {redirect_url}")
        return RedirectResponse(redirect_url)


# Получение информации о текущем пользователе
@router.get("/me", response_model=UserSchema)
async def get_me(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Убедимся, что данные в текущем пользователе валидны
    if current_user.role is None:
        current_user.role = UserRole.GUEST

    if current_user.is_approved is None:
        current_user.is_approved = False

    return current_user


# Выход из аккаунта
@router.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Successfully logged out"})
    response.delete_cookie(key="access_token")
    return response


# Тестовый эндпоинт для проверки
@router.get("/vk/callback-test")
async def vk_callback_test():
    return {"message": "Callback endpoint works!"}