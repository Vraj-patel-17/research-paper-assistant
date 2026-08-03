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