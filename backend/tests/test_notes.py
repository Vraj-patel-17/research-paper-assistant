def test_notes_workflow(client, test_paper):
    # Register
    register = client.post(
        "/users",
        json={
            "username": "noteuser",
            "email": "noteuser@example.com",
            "password": "StrongPassword123",
        },
    )
    assert register.status_code == 200

    # Login
    login = client.post(
        "/login",
        data={
            "username": "noteuser@example.com",
            "password": "StrongPassword123",
        },
    )
    assert login.status_code == 200

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    paper_id = test_paper.id

    # Create note
    create = client.post(
        f"/papers/{paper_id}/notes",
        json={"content": "Important research finding."},
        headers=headers,
    )

    assert create.status_code == 200

    note = create.json()
    note_id = note["id"]
    assert note["content"] == "Important research finding."

    # Get notes
    get = client.get(
        f"/papers/{paper_id}/notes",
        headers=headers,
    )

    assert get.status_code == 200

    notes = get.json()
    assert len(notes) == 1
    assert notes[0]["id"] == note_id

    # Update note
    update = client.put(
        f"/papers/notes/{note_id}",
        json={"content": "Updated research finding."},
        headers=headers,
    )

    assert update.status_code == 200
    assert update.json()["content"] == "Updated research finding."

    # Delete note
    delete = client.delete(
        f"/papers/notes/{note_id}",
        headers=headers,
    )

    assert delete.status_code == 204

    # Verify deletion
    get_after_delete = client.get(
        f"/papers/{paper_id}/notes",
        headers=headers,
    )

    assert get_after_delete.status_code == 200
    assert get_after_delete.json() == []
