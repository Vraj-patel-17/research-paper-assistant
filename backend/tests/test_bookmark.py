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

def test_user_cannot_access_or_delete_another_users_bookmark(
    client,
    test_paper,
):
    # User A — register
    register_a = client.post(
        "/users",
        json={
            "username": "bookmark_owner",
            "email": "bookmarkowner@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register_a.status_code == 200

    # User A — login
    login_a = client.post(
        "/login",
        data={
            "username": "bookmarkowner@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login_a.status_code == 200

    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # User A — bookmark paper
    bookmark = client.post(
        f"/bookmarks/{test_paper.id}",
        headers=headers_a,
    )

    assert bookmark.status_code == 200

    # User B — register
    register_b = client.post(
        "/users",
        json={
            "username": "bookmark_user_b",
            "email": "bookmarkuserb@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register_b.status_code == 200

    # User B — login
    login_b = client.post(
        "/login",
        data={
            "username": "bookmarkuserb@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login_b.status_code == 200

    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User B — get bookmarks
    get_bookmarks = client.get(
        "/bookmarks",
        headers=headers_b,
    )

    assert get_bookmarks.status_code == 200

    bookmarks = get_bookmarks.json()

    # User B must not see User A's bookmark
    assert all(
        bookmark["paper_id"] != test_paper.id
        for bookmark in bookmarks
    )

    # User B — attempt to delete User A's bookmark
    delete = client.delete(
        f"/bookmarks/{test_paper.id}",
        headers=headers_b,
    )

    assert delete.status_code == 404

    # User A — verify bookmark still exists
    verify = client.get(
        "/bookmarks",
        headers=headers_a,
    )

    assert verify.status_code == 200

    bookmarks = verify.json()

    assert any(
        bookmark["paper_id"] == test_paper.id
        for bookmark in bookmarks
    )

def test_duplicate_bookmark(client, auth_headers, test_paper):
    first = client.post(
        f"/bookmarks/{test_paper.id}",
        headers=auth_headers,
    )

    assert first.status_code == 200

    second = client.post(
        f"/bookmarks/{test_paper.id}",
        headers=auth_headers,
    )

    assert second.status_code == 200

    # Verify only one bookmark exists
    response = client.get(
        "/bookmarks",
        headers=auth_headers,
    )

    assert response.status_code == 200

    bookmarks = response.json()

    matching = [
        bookmark
        for bookmark in bookmarks
        if bookmark["paper_id"] == test_paper.id
    ]

    assert len(matching) == 1