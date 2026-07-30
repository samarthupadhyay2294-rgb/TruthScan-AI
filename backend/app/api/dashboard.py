from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbSession
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
async def get_dashboard(current_user: CurrentUser, db: DbSession):
    return await dashboard_service.get_dashboard(db, user_id=current_user.id)
