from fastapi import APIRouter, Depends, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.core.dependencies import CurrentUser, DbSession
from app.schemas.auth import (
    AuthUserResponse,
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    ResetPasswordRequest,
    SignupRequest,
    TokenResponse,
)
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/signup", response_model=AuthUserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def signup(request: Request, payload: SignupRequest, db: DbSession):
    return await auth_service.signup(
        db,
        email=payload.email,
        username=payload.username,
        password=payload.password,
        full_name=payload.full_name,
    )


@router.post("/login", response_model=TokenResponse)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def login(request: Request, payload: LoginRequest, db: DbSession):
    return await auth_service.login(db, email=payload.email, password=payload.password)


@router.post("/forgot-password", response_model=MessageResponse)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def forgot_password(
    request: Request, payload: ForgotPasswordRequest, db: DbSession
):
    await auth_service.forgot_password(db, email=payload.email)
    return MessageResponse(message="If the email exists, a reset link has been sent")


@router.post("/reset-password", response_model=MessageResponse)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def reset_password(request: Request, payload: ResetPasswordRequest, db: DbSession):
    await auth_service.reset_password(
        db, token=payload.token, new_password=payload.new_password
    )
    return MessageResponse(message="Password reset successful")


@router.get("/me", response_model=AuthUserResponse)
async def get_me(current_user: CurrentUser):
    return AuthUserResponse.model_validate(current_user)
