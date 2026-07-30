from typing import Annotated, AsyncGenerator

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import verify_token
from app.database.crud import get_user_by_id
from app.database.models import User
from app.database.session import async_session_factory

security_scheme = HTTPBearer(auto_error=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(security_scheme)
    ] = None,
    authorization: Annotated[str | None, Header()] = None,
) -> User:
    token: str | None = None
    if credentials:
        token = credentials.credentials
    elif authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]

    if not token:
        raise UnauthorizedError("Missing authentication token")

    user_id = verify_token(token, expected_type="access")
    if not user_id:
        raise UnauthorizedError("Invalid or expired token")

    user = await get_user_by_id(db, int(user_id))
    if not user:
        raise UnauthorizedError("User not found")
    if not user.is_active:
        raise ForbiddenError("Account is deactivated")
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


async def get_optional_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(security_scheme)
    ] = None,
    authorization: Annotated[str | None, Header()] = None,
) -> User | None:
    token: str | None = None
    if credentials:
        token = credentials.credentials
    elif authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]

    if not token:
        return None

    try:
        user_id = verify_token(token, expected_type="access")
        if not user_id:
            return None
        user = await get_user_by_id(db, int(user_id))
        if not user or not user.is_active:
            return None
        return user
    except Exception:
        return None


async def get_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_admin:
        raise ForbiddenError("Admin access required")
    return current_user


DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]
OptionalUser = Annotated[User | None, Depends(get_optional_current_user)]
AdminUser = Annotated[User, Depends(get_admin)]
