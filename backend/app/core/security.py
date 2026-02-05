import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from urllib.parse import parse_qsl
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создание JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Создание JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
    """Проверка и декодирование JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != token_type:
            return None
        return payload
    except JWTError:
        return None


def validate_telegram_auth(init_data: str) -> Optional[Dict[str, Any]]:
    """
    Валидация Telegram Web App initData согласно официальной документации
    
    Args:
        init_data: Строка initData от Telegram Web App
        
    Returns:
        Словарь с данными пользователя или None при ошибке валидации
    """
    try:
        # Парсим query string
        parsed_data = dict(parse_qsl(init_data))
        
        # Проверяем наличие обязательных полей
        if "hash" not in parsed_data:
            return None
        
        # Извлекаем hash и убираем его из данных
        received_hash = parsed_data.pop("hash")
        
        # Создаем строку для проверки подписи (все параметры кроме hash, отсортированные по ключу)
        data_check_string = "\n".join(
            f"{key}={value}" for key, value in sorted(parsed_data.items())
        )
        
        # Используем секретный ключ из настроек, если указан, иначе создаем из Bot Token
        if hasattr(settings, 'TELEGRAM_SECRET_KEY') and settings.TELEGRAM_SECRET_KEY:
            bot_token = settings.TELEGRAM_SECRET_KEY
        else:
            bot_token = settings.TELEGRAM_BOT_TOKEN
        
        # Создаем секретный ключ: HMAC_SHA256("WebAppData", bot_token)
        secret_key = hmac.new(
            key="WebAppData".encode(),
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        # Проверяем подпись: HMAC_SHA256(secret_key, data_check_string)
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        if calculated_hash != received_hash:
            return None
        
        # Проверяем время (auth_date не должен быть старше 24 часов)
        auth_date = int(parsed_data.get("auth_date", 0))
        current_timestamp = datetime.now().timestamp()
        if current_timestamp - auth_date > 86400:  # 24 часа
            return None
        
        # Извлекаем данные пользователя
        user_data = {}
        if "user" in parsed_data:
            import json
            user_data = json.loads(parsed_data["user"])
        
        return {
            "id": user_data.get("id"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "username": user_data.get("username"),
            "language_code": user_data.get("language_code"),
            "is_premium": user_data.get("is_premium", False),
            "auth_date": auth_date,
        }
    except Exception as e:
        # В production здесь нужно логировать ошибку
        print(f"Error validating Telegram auth: {e}")
        return None
