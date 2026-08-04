def test_get_bookmarks_without_token(client):
    response = client.get("/bookmarks")

    assert response.status_code == 401

def test_get_bookmarks_invalid_token(client):
    headers = {
        "Authorization": "Bearer invalid_token"
    }

    response = client.get("/bookmarks", headers=headers)

    assert response.status_code == 401

def test_bookmark_invalid_paper_id(client, auth_headers):
    response = client.post(
        "/bookmarks/0",
        headers=auth_headers,
    )

    assert response.status_code == 422

def test_delete_bookmark_invalid_paper_id(client, auth_headers):
    response = client.delete(
        "/bookmarks/-1",
        headers=auth_headers,
    )

    assert response.status_code == 422

def test_bookmark_nonexistent_paper(client, auth_headers):
    response = client.post(
        "/bookmarks/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404
    

def test_delete_nonexistent_bookmark(client, auth_headers):
    response = client.delete(
        "/bookmarks/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404
    