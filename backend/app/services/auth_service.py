from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictError, NotFoundError, UnauthorizedError
from app.core.security import (
    create_access_token,
    create_password_reset_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from app.database import crud
from app.schemas.auth import AuthUserResponse, TokenResponse
from app.services.email_service import send_password_reset_email


class AuthService:
    async def signup(
        self,
        db: AsyncSession,
        *,
        email: str,
        username: str,
        password: str,
        full_name: str | None = None,
    ) -> AuthUserResponse:
        if await crud.get_user_by_email(db, email):
            raise ConflictError("Email already registered")
        if await crud.get_user_by_username(db, username):
            raise ConflictError("Username already taken")

        user = await crud.create_user(
            db,
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            full_name=full_name,
        )
        return AuthUserResponse.model_validate(user)

    async def login(self, db: AsyncSession, *, email: str, password: str) -> TokenResponse:
        user = await crud.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("Account is deactivated")

        token = create_access_token(user.id)
        return TokenResponse(
            access_token=token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def forgot_password(self, db: AsyncSession, *, email: str) -> None:
        user = await crud.get_user_by_email(db, email)
        if not user:
            return

        await crud.invalidate_user_password_reset_tokens(db, user.id)
        token = create_password_reset_token(user.email)
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
        )
        await crud.create_password_reset_token(db, user.id, token, expires_at)
        await send_password_reset_email(email=user.email, token=token)

    async def reset_password(
        self, db: AsyncSession, *, token: str, new_password: str
    ) -> None:
        email = verify_token(token, expected_type="password_reset")
        if not email:
            raise UnauthorizedError("Invalid or expired reset token")

        reset_record = await crud.get_valid_password_reset_token(db, token)
        if not reset_record:
            raise UnauthorizedError("Invalid or expired reset token")

        user = await crud.get_user_by_email(db, email)
        if not user:
            raise NotFoundError("User not found")

        await crud.update_user(
            db, user, hashed_password=get_password_hash(new_password)
        )
        await crud.mark_password_reset_token_used(db, reset_record.id)


auth_service = AuthService()
