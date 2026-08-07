def test_get_papers(client):
    response = client.get("/papers")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert "has_next" in data

def test_get_papers_invalid_limit(client):
    response = client.get("/papers?limit=0")

    assert response.status_code == 422

def test_get_invalid_paper_id(client):
    response = client.get("/papers/0")

    assert response.status_code == 422

def test_get_nonexistent_paper(client):
    response = client.get("/papers/999999")

    assert response.status_code == 404

def test_get_papers_pagination(client):
    response = client.get("/papers?limit=2&offset=0")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert data["limit"] == 2
    assert data["offset"] == 0
    assert "has_next" in data
def test_get_papers_invalid_limit(client):
    response = client.get("/papers?limit=101")

    assert response.status_code == 422
def test_get_papers_invalid_offset(client):
    response = client.get("/papers?offset=-1")

    assert response.status_code == 422
def test_get_papers_sort_latest(client):
    response = client.get("/papers?sort=latest")

    assert response.status_code == 200
def test_get_papers_sort_oldest(client):
    response = client.get("/papers?sort=oldest")

    assert response.status_code == 200
def test_get_papers_sort_title(client):
    response = client.get("/papers?sort=title")

    assert response.status_code == 200
def test_get_papers_invalid_sort(client):
    response = client.get("/papers?sort=random")

    assert response.status_code == 422