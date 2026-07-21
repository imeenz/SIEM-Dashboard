import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "analyst@example.com",
            "password": "SecurePassword123!",
            "full_name": "SOC Analyst",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "analyst@example.com"
    assert data["full_name"] == "SOC Analyst"
    assert data["is_active"] is True
    assert "hashed_password" not in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "email": "analyst@example.com",
        "password": "SecurePassword123!",
        "full_name": "SOC Analyst",
    }

    first_response = await client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_login_returns_access_token(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "SecurePassword123!",
            "full_name": "SOC Analyst",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


@pytest.mark.asyncio
async def test_login_rejects_wrong_password(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "wronglogin@example.com",
            "password": "SecurePassword123!",
            "full_name": "SOC Analyst",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "wronglogin@example.com",
            "password": "WrongPassword!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
@pytest.mark.asyncio
async def test_get_current_user(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "me@example.com",
            "password": "SecurePassword123!",
            "full_name": "SOC Analyst",
        },
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "me@example.com",
            "password": "SecurePassword123!",
        },
    )

    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "me@example.com"
    assert data["full_name"] == "SOC Analyst"


@pytest.mark.asyncio
async def test_get_current_user_rejects_invalid_token(client):
    response = await client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
@pytest.mark.asyncio
async def test_events_require_authentication(client):
    response = await client.get(
        "/api/v1/events"
    )

    assert response.status_code in (401, 403)
@pytest.mark.asyncio
async def test_authenticated_user_can_access_events(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "events@example.com",
            "password": "SecurePassword123!",
            "full_name": "SOC Analyst",
        },
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "events@example.com",
            "password": "SecurePassword123!",
        },
    )

    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/events",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200