from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies import get_current_active_user
from ..models import SubscriptionPlan, User
from ..schemas import (
    CardInsight,
    CompatibilityInsight,
    CompatibilityRequest,
    ForecastResponse,
    PersonalBlueprint,
)
from ..services.card_science import (
    build_compatibility_theme,
    build_yearly_cycles,
    compatibility_lessons,
    compatibility_score,
    derive_personal_blueprint,
    draw_today_card,
)

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/personal", response_model=PersonalBlueprint)
async def get_personal_insight(current_user: User = Depends(get_current_active_user)) -> PersonalBlueprint:
    if not current_user.profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="请先填写生日信息")
    blueprint = derive_personal_blueprint(current_user.profile.birth_date)
    return blueprint


@router.get("/forecast", response_model=ForecastResponse)
async def get_full_forecast(current_user: User = Depends(get_current_active_user)) -> ForecastResponse:
    if current_user.subscription_plan != SubscriptionPlan.PREMIUM:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="升级为付费订阅以查看完整分析")
    if not current_user.profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="请先填写生日信息")

    birthday = current_user.profile.birth_date
    blueprint = derive_personal_blueprint(birthday)
    cycles = build_yearly_cycles(birthday)
    today = draw_today_card(birthday)

    return ForecastResponse(personal_blueprint=blueprint, yearly_cycles=cycles, today_card=today)


@router.get("/today", response_model=CardInsight)
async def get_today_card(current_user: User = Depends(get_current_active_user)) -> CardInsight:
    if current_user.subscription_plan != SubscriptionPlan.PREMIUM:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="升级为付费订阅以查看今日牌")
    if not current_user.profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="请先填写生日信息")
    return draw_today_card(current_user.profile.birth_date)


@router.post("/compatibility", response_model=CompatibilityInsight)
async def get_compatibility(
    payload: CompatibilityRequest,
    current_user: User = Depends(get_current_active_user),
) -> CompatibilityInsight:
    if current_user.subscription_plan != SubscriptionPlan.PREMIUM:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="升级为付费订阅以查看合盘")
    if not current_user.profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="请先填写生日信息")

    birthday = current_user.profile.birth_date
    score = compatibility_score(birthday, payload.partner_birth_date)
    lessons = compatibility_lessons(birthday, payload.partner_birth_date)
    theme = build_compatibility_theme(birthday, payload.partner_birth_date)

    return CompatibilityInsight(
        compatibility_score=score,
        shared_lessons=lessons[:2],
        growth_opportunities=lessons[2:],
        relationship_theme=theme,
    )
