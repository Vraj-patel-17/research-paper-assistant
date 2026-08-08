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
            "paper_id": test_paper.id,
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
        paper["id"] == test_paper.id
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
        paper["id"] != test_paper.id
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