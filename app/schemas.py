from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from .models import SubscriptionPlan


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)
    birth_date: date
    timezone: Optional[str] = "UTC"


class UserUpdate(BaseModel):
    full_name: Optional[str]
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    timezone: Optional[str]


class UserRead(UserBase):
    id: int
    subscription_plan: SubscriptionPlan
    created_at: datetime

    class Config:
        orm_mode = True


class BirthProfileRead(BaseModel):
    birth_date: date
    timezone: Optional[str]
    preferred_deck: Optional[str]

    class Config:
        orm_mode = True


class SubscriptionStatus(BaseModel):
    plan: SubscriptionPlan
    renewed_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CompatibilityRequest(BaseModel):
    partner_birth_date: date


class CardInsight(BaseModel):
    title: str
    description: str
    advice: str


class PersonalBlueprint(BaseModel):
    life_card: CardInsight
    ruling_card: CardInsight
    soul_resource_card: Optional[CardInsight]
    soul_challenge_card: Optional[CardInsight]
    is_special_family: bool = False


class CycleInsight(BaseModel):
    cycle_index: int
    cycle_start: date
    cycle_end: date
    theme: str
    advice: str


class ForecastResponse(BaseModel):
    personal_blueprint: PersonalBlueprint
    yearly_cycles: list[CycleInsight]
    today_card: CardInsight


class CompatibilityInsight(BaseModel):
    compatibility_score: int
    shared_lessons: list[str]
    growth_opportunities: list[str]
    relationship_theme: str


class SubscriptionUpdate(BaseModel):
    plan: SubscriptionPlan


class EmailPreferenceRead(BaseModel):
    daily_digest_enabled: bool
    cycle_digest_enabled: bool
    last_daily_sent: Optional[datetime]
    last_cycle_sent: Optional[datetime]

    class Config:
        orm_mode = True


class EmailPreferenceUpdate(BaseModel):
    daily_digest_enabled: Optional[bool]
    cycle_digest_enabled: Optional[bool]
