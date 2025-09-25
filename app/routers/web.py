from datetime import datetime
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..dependencies import get_current_active_user
from ..models import SubscriptionPlan, User
from ..services.card_science import derive_personal_blueprint

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "year": datetime.utcnow().year})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_user: User = Depends(get_current_active_user),
) -> HTMLResponse:
    profile = current_user.profile
    blueprint = derive_personal_blueprint(profile.birth_date) if profile else None
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "blueprint": blueprint,
            "is_premium": current_user.subscription_plan == SubscriptionPlan.PREMIUM,
        },
    )
