from .conftest import client

def test_application_starts():
    response = client.get("/health/live")
    assert response.status_code == 200