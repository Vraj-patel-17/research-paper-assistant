def test_collections_workflow(client, test_paper):

    # Step 1: Register
    register = client.post(
        "/users",
        json={
            "username": "collectionuser",
            "email": "collectionuser@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register.status_code == 200

    # Step 2: Login
    login = client.post(
        "/login",
        data={
            "username": "collectionuser@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Create collection
    create = client.post(
        "/collections",
        json={
            "name": "My Research",
        },
        headers=headers,
    )

    assert create.status_code == 201

    collection = create.json()
    collection_id = collection["id"]

    assert collection["name"] == "My Research"

    # Step 4: Get collections
    get_collections = client.get(
        "/collections",
        headers=headers,
    )

    assert get_collections.status_code == 200

    collections = get_collections.json()

    assert any(
        collection["id"] == collection_id
        for collection in collections
    )

    # Step 5: Get specific collection
    get_collection = client.get(
        f"/collections/{collection_id}",
        headers=headers,
    )

    assert get_collection.status_code == 200
    assert get_collection.json()["id"] == collection_id

    # Step 6: Add paper to collection
    add_paper = client.post(
        f"/collections/{collection_id}/papers",
        json={
            "paper_id": str(test_paper.id),
        },
        headers=headers,
    )

    assert add_paper.status_code == 201

    # Step 7: Get collection papers
    get_papers = client.get(
        f"/collections/{collection_id}/papers",
        headers=headers,
    )

    assert get_papers.status_code == 200

    papers = get_papers.json()

    assert any(
        paper["id"] == str(test_paper.id)
        for paper in papers
    )

    # Step 8: Remove paper
    remove_paper = client.delete(
        f"/collections/{collection_id}/papers/{test_paper.id}",
        headers=headers,
    )

    assert remove_paper.status_code == 204

    # Step 9: Verify paper removed
    get_papers_after_remove = client.get(
        f"/collections/{collection_id}/papers",
        headers=headers,
    )

    assert get_papers_after_remove.status_code == 200

    assert all(
        paper["id"] != str(test_paper.id)
        for paper in get_papers_after_remove.json()
    )

    # Step 10: Delete collection
    delete = client.delete(
        f"/collections/{collection_id}",
        headers=headers,
    )

    assert delete.status_code == 204

    # Step 11: Verify collection deleted
    get_deleted = client.get(
        f"/collections/{collection_id}",
        headers=headers,
    )

    assert get_deleted.status_code == 404


def test_user_cannot_access_another_users_collection(client):

    # User A — register
    register_a = client.post(
        "/users",
        json={
            "username": "user_a",
            "email": "usera@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register_a.status_code == 200

    # User A — login
    login_a = client.post(
        "/login",
        data={
            "username": "usera@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login_a.status_code == 200

    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # User A — create collection
    create = client.post(
        "/collections",
        json={"name": "Private Collection"},
        headers=headers_a,
    )

    assert create.status_code == 201

    collection_id = create.json()["id"]

    # User B — register
    register_b = client.post(
        "/users",
        json={
            "username": "user_b",
            "email": "userb@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register_b.status_code == 200

    # User B — login
    login_b = client.post(
        "/login",
        data={
            "username": "userb@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login_b.status_code == 200

    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User B — attempt to access User A's collection
    response = client.get(
        f"/collections/{collection_id}",
        headers=headers_b,
    )

    assert response.status_code == 404


def test_user_cannot_modify_or_delete_another_users_collection(
    client,
    test_paper,
):

    # User A — register
    register_a = client.post(
        "/users",
        json={
            "username": "owner",
            "email": "owner@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register_a.status_code == 200

    # User A — login
    login_a = client.post(
        "/login",
        data={
            "username": "owner@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login_a.status_code == 200

    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # User A — create collection
    create = client.post(
        "/collections",
        json={"name": "Owner Collection"},
        headers=headers_a,
    )

    assert create.status_code == 201

    collection_id = create.json()["id"]

    # User B — register
    register_b = client.post(
        "/users",
        json={
            "username": "attacker",
            "email": "attacker@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register_b.status_code == 200

    # User B — login
    login_b = client.post(
        "/login",
        data={
            "username": "attacker@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login_b.status_code == 200

    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User B — attempt to add a paper
    add_paper = client.post(
        f"/collections/{collection_id}/papers",
        json={
            "paper_id": str(test_paper.id),
        },
        headers=headers_b,
    )

    assert add_paper.status_code == 404

    # User B — attempt to remove a paper
    remove_paper = client.delete(
        f"/collections/{collection_id}/papers/{test_paper.id}",
        headers=headers_b,
    )

    assert remove_paper.status_code == 404

    # User B — attempt to delete collection
    delete = client.delete(
        f"/collections/{collection_id}",
        headers=headers_b,
    )

    assert delete.status_code == 404

    # User A — verify collection still exists
    verify = client.get(
        f"/collections/{collection_id}",
        headers=headers_a,
    )

    assert verify.status_code == 200
    assert verify.json()["id"] == collection_id


def test_duplicate_collection_name(client):

    # Register
    register = client.post(
        "/users",
        json={
            "username": "dupcollectionuser",
            "email": "dupcollection@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register.status_code == 200

    # Login
    login = client.post(
        "/login",
        data={
            "username": "dupcollection@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # First collection
    first = client.post(
        "/collections",
        json={
            "name": "Research Papers",
        },
        headers=headers,
    )

    assert first.status_code == 201

    # Duplicate collection
    second = client.post(
        "/collections",
        json={
            "name": "Research Papers",
        },
        headers=headers,
    )

    assert second.status_code in (201, 400, 409)

