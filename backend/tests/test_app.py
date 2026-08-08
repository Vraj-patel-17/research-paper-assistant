

def test_application_starts(client):
    response = client.get("/health/live")
    assert response.status_code == 200