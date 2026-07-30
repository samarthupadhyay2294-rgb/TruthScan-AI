import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_signup(client: AsyncClient):
    response = await client.post(
        "/api/auth/signup",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "SecurePass123",
            "full_name": "New User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data


@pytest.mark.asyncio
async def test_signup_duplicate_email(client: AsyncClient, test_user):
    response = await client.post(
        "/api/auth/signup",
        json={
            "email": test_user.email,
            "username": "anotheruser",
            "password": "SecurePass123",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user):
    response = await client.post(
        "/api/auth/login",
        json={"email": test_user.email, "password": "TestPass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, test_user):
    response = await client.post(
        "/api/auth/login",
        json={"email": test_user.email, "password": "WrongPassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, test_user, auth_headers):
    response = await client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username


@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    response = await client.get("/api/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_forgot_password(client: AsyncClient, test_user):
    response = await client.post(
        "/api/auth/forgot-password",
        json={"email": test_user.email},
    )
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_reset_password(client: AsyncClient, test_user, db_session):
    from datetime import datetime, timedelta, timezone

    from app.core.security import create_password_reset_token
    from app.database import crud

    token = create_password_reset_token(test_user.email)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    await crud.create_password_reset_token(db_session, test_user.id, token, expires_at)
    await db_session.commit()

    response = await client.post(
        "/api/auth/reset-password",
        json={"token": token, "new_password": "NewSecurePass123"},
    )
    assert response.status_code == 200

    login_response = await client.post(
        "/api/auth/login",
        json={"email": test_user.email, "password": "NewSecurePass123"},
    )
    assert login_response.status_code == 200
