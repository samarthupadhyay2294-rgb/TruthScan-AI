from fastapi import APIRouter

from app.api import admin, auth, dashboard, history, prediction, reports, users

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(prediction.router)
api_router.include_router(prediction.upload_router)
api_router.include_router(dashboard.router)
api_router.include_router(history.router)
api_router.include_router(reports.router)
api_router.include_router(admin.router)
