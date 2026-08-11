def test_security_headers(client):
    response = client.get("/papers")

    assert response.status_code == 200

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"

    assert response.headers["Permissions-Policy"] == (
        "camera=(), "
        "microphone=(), "
        "geolocation=(), "
        "payment=(), "
        "usb=()"
    )

    assert response.headers["Cross-Origin-Opener-Policy"] == "same-origin"
    assert response.headers["Cross-Origin-Resource-Policy"] == "same-origin"