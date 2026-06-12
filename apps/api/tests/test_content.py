VALID_YOUTUBE_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def test_ingest_success(client, user_headers):
    resp = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": VALID_YOUTUBE_URL, "platform": "youtube", "title": "Test Video"},
        headers=user_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["source_url"] == VALID_YOUTUBE_URL
    assert data["status"] == "pending"
    assert data["title"] == "Test Video"


def test_ingest_unauthorized(client):
    resp = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": VALID_YOUTUBE_URL, "platform": "youtube"},
    )
    assert resp.status_code == 401


def test_ingest_invalid_url(client, user_headers):
    resp = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": "https://example.com/video", "platform": "youtube"},
        headers=user_headers,
    )
    assert resp.status_code == 400
    assert "Only YouTube" in resp.json()["detail"]


def test_ingest_dedup(client, user_headers):
    resp1 = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": VALID_YOUTUBE_URL, "platform": "youtube"},
        headers=user_headers,
    )
    assert resp1.status_code == 200

    resp2 = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": VALID_YOUTUBE_URL, "platform": "youtube"},
        headers=user_headers,
    )
    assert resp2.status_code == 200
    assert resp2.json()["id"] == resp1.json()["id"]


def test_list_content_empty(client, user_headers):
    resp = client.get("/api/content", headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_list_content_with_data(client, user_headers):
    client.post(
        "/api/ingest/browser-capture",
        json={"source_url": VALID_YOUTUBE_URL, "platform": "youtube"},
        headers=user_headers,
    )
    resp = client.get("/api/content", headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_list_content_pagination(client, user_headers):
    for i in range(5):
        client.post(
            "/api/ingest/browser-capture",
            json={"source_url": f"https://www.youtube.com/watch?v=vid{i:06d}", "platform": "youtube"},
            headers=user_headers,
        )
    resp = client.get("/api/content?offset=0&limit=2", headers=user_headers)
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["offset"] == 0
    assert data["limit"] == 2


def test_get_content_detail(client, user_headers):
    create = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": VALID_YOUTUBE_URL, "platform": "youtube"},
        headers=user_headers,
    )
    content_id = create.json()["id"]
    resp = client.get(f"/api/content/{content_id}", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == content_id


def test_get_content_not_found(client, user_headers):
    resp = client.get("/api/content/00000000-0000-0000-0000-000000000000", headers=user_headers)
    assert resp.status_code == 404


def test_get_content_not_owner(client, user_headers, second_user_headers):
    create = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": VALID_YOUTUBE_URL, "platform": "youtube"},
        headers=user_headers,
    )
    content_id = create.json()["id"]
    resp = client.get(f"/api/content/{content_id}", headers=second_user_headers)
    assert resp.status_code == 403


def test_daily_limit_enforced(client, user_headers):
    from app.config import get_settings

    limit = get_settings().free_daily_ingest_limit
    for i in range(limit):
        client.post(
            "/api/ingest/browser-capture",
            json={"source_url": f"https://www.youtube.com/watch?v=vid{i:06d}", "platform": "youtube"},
            headers=user_headers,
        )
    resp = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": "https://www.youtube.com/watch?v=overflow", "platform": "youtube"},
        headers=user_headers,
    )
    assert resp.status_code == 429
    assert "limit" in resp.json()["detail"].lower()
