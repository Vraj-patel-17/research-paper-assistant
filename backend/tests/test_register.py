def test_register_success(client):
    response = client.post(
        "/users",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPassword123"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data
def test_register_duplicate_email(client):
    payload = {
        "username":"duplicate",
        "email": "duplicate@example.com",
        "password": "StrongPassword123",
    }

    client.post("/users", json=payload)

    response = client.post("/users", json=payload)

    assert response.status_code in (400, 409)
def test_register_invalid_email(client):
    response = client.post(
        "/users",
        json={
            "username":"user123",
            "email": "not-an-email",
            "password": "StrongPassword123",
           
        },
    )

    assert response.status_code == 422

def test_register_missing_password(client):
    response = client.post(
        "/users",
        json={
            "username":"user123",
            "email": "user@example.com",
        },
    )

    assert response.status_code == 422
def test_create_user_duplicate_email(client):
    payload = {
        "username": "john",
        "email": "john@example.com",
        "password": "StrongPassword123",
    }

    client.post("/users", json=payload)
    response = client.post(
        "/users",
        json={
            "username": "john2",
            "email": "john@example.com",
            "password": "StrongPassword123",
        },
    )

    assert response.status_code == 409
    