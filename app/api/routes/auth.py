from fastapi import HTTPException, status, Depends
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse,TokenResponse
from app.db.session import get_db
from app.core.security import verify_password, hash_password, create_access_token
from app.logger import logger

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/register')
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:

    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        logger.warning(f"Registration attempt with existing email: {user_data.email}")
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        full_name=str(user_data.full_name),
        email=str(user_data.email),
        hashed_password=hash_password(user_data.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    logger.info(f"New user registered: {new_user.email}")

    return UserResponse.model_validate(new_user)


@router.post('/login')
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    query = select(User).where(User.email == form_data.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = create_access_token(str(user.id))
    logger.info(f"User logged in: {user.email}")
    return TokenResponse(access_token=token, token_type="bearer")