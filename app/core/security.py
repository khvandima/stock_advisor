from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
from jose import jwt

from app.logger import logger
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain: str, hashed_password: str) -> bool:
    if not pwd_context.verify(plain, hashed_password):
        logger.error(f"Password incorrect")
        return False
    return True


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
