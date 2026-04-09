from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from app.config import settings

from app.db.models import User
from app.db.session import get_db

from app.logger import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):

    try:
        user_id = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]).get("sub")
        logger.info(f"Token decoded, user_id: {user_id}")
    except JWTError:
        logger.error("JWT decode failed: invalid token")
        raise HTTPException(status_code=401)
    if not user_id:
        logger.error("JWT token has no subject claim")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(status_code=401, detail="User not found")
    logger.info(f"User authenticated: {user.id}")

    return user
