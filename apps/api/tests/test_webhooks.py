def test_create_webhook(client, user_headers):
    resp = client.post(
        "/api/webhooks",
        json={"url": "https://example.com/webhook", "events": ["content.captured"]},
        headers=user_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["url"] == "https://example.com/webhook"
    assert data["events"] == ["content.captured"]
    assert data["is_active"] is True


def test_list_webhooks_empty(client, user_headers):
    resp = client.get("/api/webhooks", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_webhooks_with_data(client, user_headers):
    client.post(
        "/api/webhooks",
        json={"url": "https://example.com/hook1", "events": ["*"]},
        headers=user_headers,
    )
    client.post(
        "/api/webhooks",
        json={"url": "https://example.com/hook2", "events": ["plan.created"]},
        headers=user_headers,
    )
    resp = client.get("/api/webhooks", headers=user_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_delete_webhook(client, user_headers):
    create = client.post(
        "/api/webhooks",
        json={"url": "https://example.com/webhook", "events": ["*"]},
        headers=user_headers,
    )
    webhook_id = create.json()["id"]
    resp = client.delete(f"/api/webhooks/{webhook_id}", headers=user_headers)
    assert resp.status_code == 204

    list_resp = client.get("/api/webhooks", headers=user_headers)
    assert len(list_resp.json()) == 0


def test_delete_webhook_not_found(client, user_headers):
    resp = client.delete(
        "/api/webhooks/00000000-0000-0000-0000-000000000000",
        headers=user_headers,
    )
    assert resp.status_code == 404


def test_webhooks_isolation(client, user_headers, second_user_headers):
    client.post(
        "/api/webhooks",
        json={"url": "https://example.com/hook1", "events": ["*"]},
        headers=user_headers,
    )
    resp = client.get("/api/webhooks", headers=second_user_headers)
    assert resp.json() == []


def test_webhook_unauthorized(client):
    resp = client.post(
        "/api/webhooks",
        json={"url": "https://example.com/webhook", "events": ["*"]},
    )
    assert resp.status_code == 401
