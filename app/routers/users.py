from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session
from ..dependencies import get_current_active_user
from ..models import BirthProfile, EmailPreference, SubscriptionPlan, User
from ..schemas import (
    BirthProfileRead,
    EmailPreferenceRead,
    EmailPreferenceUpdate,
    SubscriptionStatus,
    SubscriptionUpdate,
    UserRead,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_active_user)) -> UserRead:
    return UserRead.from_orm(current_user)


@router.patch("/me", response_model=UserRead)
async def update_me(
    payload: UserUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> UserRead:
    if payload.full_name is not None:
        current_user.full_name = payload.full_name
    if payload.password:
        from ..core.security import get_password_hash

        current_user.hashed_password = get_password_hash(payload.password)
    if payload.timezone and current_user.profile:
        current_user.profile.timezone = payload.timezone

    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)
    return UserRead.from_orm(current_user)


@router.get("/me/profile", response_model=BirthProfileRead)
async def get_profile(current_user: User = Depends(get_current_active_user)) -> BirthProfileRead:
    if not current_user.profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile missing")
    return BirthProfileRead.from_orm(current_user.profile)


@router.get("/me/subscription", response_model=SubscriptionStatus)
async def get_subscription(current_user: User = Depends(get_current_active_user)) -> SubscriptionStatus:
    return SubscriptionStatus(plan=current_user.subscription_plan, renewed_at=current_user.updated_at)


@router.post("/me/subscription", response_model=SubscriptionStatus)
async def update_subscription(
    payload: SubscriptionUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> SubscriptionStatus:
    if payload.plan == current_user.subscription_plan:
        return SubscriptionStatus(plan=current_user.subscription_plan, renewed_at=current_user.updated_at)

    current_user.subscription_plan = payload.plan
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)
    return SubscriptionStatus(plan=current_user.subscription_plan, renewed_at=current_user.updated_at)


@router.get("/me/email-preferences", response_model=EmailPreferenceRead)
async def get_email_preferences(current_user: User = Depends(get_current_active_user)) -> EmailPreferenceRead:
    if not current_user.email_preferences:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferences missing")
    return EmailPreferenceRead.from_orm(current_user.email_preferences)


@router.patch("/me/email-preferences", response_model=EmailPreferenceRead)
async def update_email_preferences(
    payload: EmailPreferenceUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> EmailPreferenceRead:
    preferences = current_user.email_preferences
    if not preferences:
        preferences = EmailPreference(user_id=current_user.id)

    if payload.daily_digest_enabled is not None:
        preferences.daily_digest_enabled = payload.daily_digest_enabled
    if payload.cycle_digest_enabled is not None:
        preferences.cycle_digest_enabled = payload.cycle_digest_enabled

    session.add(preferences)
    await session.commit()
    await session.refresh(preferences)
    return EmailPreferenceRead.from_orm(preferences)
