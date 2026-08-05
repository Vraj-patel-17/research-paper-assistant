def test_get_papers(client):
    response = client.get("/papers")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_papers_invalid_limit(client):
    response = client.get("/papers?limit=0")

    assert response.status_code == 422

def test_get_invalid_paper_id(client):
    response = client.get("/papers/0")

    assert response.status_code == 422

def test_get_nonexistent_paper(client):
    response = client.get("/papers/999999")

    assert response.status_code == 404