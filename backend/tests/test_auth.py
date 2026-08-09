from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def test_login_success(client, test_user):
    response = client.post(
    "/login",
    data={
        "username": "test@example.com",
        "password": "password123",
    },
)

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "wrongpassword",
        },
    )

    print(response.status_code)
    print(response.json())

def test_get_me(client, auth_headers):
    response = client.get(
        "/me",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

def test_protected_endpoint_without_token(client):
    response = client.get("/bookmarks")

    assert response.status_code == 401


def test_protected_endpoint_malformed_auth_header(client):
    headers = {
        "Authorization": "NotBearerToken"
    }

    response = client.get("/bookmarks", headers=headers)

    assert response.status_code == 401

def test_protected_endpoint_with_expired_token(client):
    expired_token = jwt.encode(
        {
            "sub": "test@example.com",
            "exp": datetime.utcnow() - timedelta(minutes=1),
        },
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    headers = {
        "Authorization": f"Bearer {expired_token}"
    }

    response = client.get(
        "/bookmarks",
        headers=headers,
    )

    assert response.status_code == 401