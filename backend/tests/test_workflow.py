def test_user_bookmark_workflow(client,test_paper):
    paper_id=test_paper.id
    # Step 1: Register user
    register = client.post(
        "/users",
        json={
            "username": "workflowuser",
            "email": "workflow@example.com",
            "password": "StrongPassword123",
        },
    )
    assert register.status_code == 200

    # Step 2: Login
    login = client.post(
        "/login",
        data={
            "username": "workflow@example.com",
            "password": "StrongPassword123",
        },
    )
    assert login.status_code == 200

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Get papers
 

    assert test_paper.id is not None

    paper_id = test_paper.id

    # Step 4: Bookmark paper
    bookmark = client.post(
        f"/bookmarks/{paper_id}",
        headers=headers,
    )
    assert bookmark.status_code == 200

    # Step 5: Verify bookmark exists
    bookmarks = client.get(
        "/bookmarks",
        headers=headers,
    )
    assert bookmarks.status_code == 200

    bookmarks = bookmarks.json()
    assert any(b["paper_id"] == paper_id for b in bookmarks)

    # Step 6: Delete bookmark
    delete = client.delete(
        f"/bookmarks/{paper_id}",
        headers=headers,
    )
    assert delete.status_code == 200

    # Step 7: Verify bookmark removed
    bookmarks = client.get(
        "/bookmarks",
        headers=headers,
    )

    bookmarks = bookmarks.json()
    assert all(b["paper_id"] != paper_id for b in bookmarks)