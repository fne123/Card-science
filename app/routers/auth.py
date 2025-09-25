from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..core.security import create_access_token, get_password_hash, verify_password
from ..database import get_session
from ..models import BirthProfile, EmailPreference, SubscriptionPlan, User
from ..schemas import LoginRequest, Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate, session: AsyncSession = Depends(get_session)
) -> UserRead:
    existing_user = await session.scalar(select(User).where(User.email == payload.email))
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已被注册")

    user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
        subscription_plan=SubscriptionPlan.FREE,
        created_at=datetime.utcnow(),
    )
    session.add(user)
    await session.flush()

    profile = BirthProfile(user_id=user.id, birth_date=payload.birth_date, timezone=payload.timezone)
    preferences = EmailPreference(user_id=user.id)
    session.add_all([profile, preferences])
    await session.commit()
    await session.refresh(user)

    return UserRead.from_orm(user)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> Token:
    user = await session.scalar(select(User).where(User.email == form_data.username))
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱或密码错误")

    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)


@router.post("/login/json", response_model=Token)
async def login_with_json(payload: LoginRequest, session: AsyncSession = Depends(get_session)) -> Token:
    user = await session.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱或密码错误")

    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)
