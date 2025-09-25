import enum
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class SubscriptionPlan(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]
    full_name: Mapped[Optional[str]]
    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        Enum(SubscriptionPlan), default=SubscriptionPlan.FREE, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    profile: Mapped["BirthProfile"] = relationship(
        "BirthProfile", back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    email_preferences: Mapped["EmailPreference"] = relationship(
        "EmailPreference", back_populates="user", cascade="all, delete-orphan", uselist=False
    )


class BirthProfile(Base):
    __tablename__ = "birth_profiles"
    __table_args__ = (UniqueConstraint("user_id", name="uq_birth_profile_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    timezone: Mapped[Optional[str]] = mapped_column(String(64))
    preferred_deck: Mapped[Optional[str]] = mapped_column(String(32), default="standard")

    user: Mapped[User] = relationship("User", back_populates="profile")


class EmailPreference(Base):
    __tablename__ = "email_preferences"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    daily_digest_enabled: Mapped[bool] = mapped_column(default=True)
    cycle_digest_enabled: Mapped[bool] = mapped_column(default=True)
    last_daily_sent: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_cycle_sent: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    user: Mapped[User] = relationship("User", back_populates="email_preferences")
