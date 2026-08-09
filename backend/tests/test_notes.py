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

def test_user_cannot_access_or_modify_another_users_note(
    client,
    test_paper,
):
    # User A — register
    register_a = client.post(
        "/users",
        json={
            "username": "note_owner",
            "email": "noteowner@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register_a.status_code == 200

    # User A — login
    login_a = client.post(
        "/login",
        data={
            "username": "noteowner@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login_a.status_code == 200

    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # User A — create note
    create = client.post(
        f"/papers/{test_paper.id}/notes",
        json={"content": "Private research note."},
        headers=headers_a,
    )

    assert create.status_code == 200

    note_id = create.json()["id"]

    # User B — register
    register_b = client.post(
        "/users",
        json={
            "username": "note_attacker",
            "email": "noteattacker@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register_b.status_code == 200

    # User B — login
    login_b = client.post(
        "/login",
        data={
            "username": "noteattacker@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login_b.status_code == 200

    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User B — attempt to view User A's notes
    get_notes = client.get(
        f"/papers/{test_paper.id}/notes",
        headers=headers_b,
    )

    assert get_notes.status_code == 200
    assert all(
        note["id"] != note_id
        for note in get_notes.json()
    )

    # User B — attempt to update User A's note
    update = client.put(
        f"/papers/notes/{note_id}",
        json={"content": "Malicious update."},
        headers=headers_b,
    )

    assert update.status_code == 404

    # User B — attempt to delete User A's note
    delete = client.delete(
        f"/papers/notes/{note_id}",
        headers=headers_b,
    )

    assert delete.status_code == 404

    # User A — verify the note still exists and was not modified
    verify = client.get(
        f"/papers/{test_paper.id}/notes",
        headers=headers_a,
    )

    assert verify.status_code == 200

    notes = verify.json()

    assert len(notes) == 1
    assert notes[0]["id"] == note_id
    assert notes[0]["content"] == "Private research note."