def test_get_settings_defaults(client, user_headers):
    resp = client.get("/api/settings", headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["gatekeeper_enabled"] is False
    assert data["gatekeeper_threshold"] == 70


def test_update_settings(client, user_headers):
    resp = client.patch(
        "/api/settings",
        json={"gatekeeper_enabled": True, "gatekeeper_threshold": 85},
        headers=user_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["gatekeeper_enabled"] is True
    assert data["gatekeeper_threshold"] == 85


def test_update_settings_threshold_bounds(client, user_headers):
    resp = client.patch(
        "/api/settings",
        json={"gatekeeper_enabled": True, "gatekeeper_threshold": 5},
        headers=user_headers,
    )
    assert resp.status_code == 422


def test_settings_unauthorized(client):
    resp = client.get("/api/settings")
    assert resp.status_code == 401


def test_settings_persist_across_requests(client, user_headers):
    client.patch(
        "/api/settings",
        json={"gatekeeper_enabled": True, "gatekeeper_threshold": 50},
        headers=user_headers,
    )
    resp = client.get("/api/settings", headers=user_headers)
    assert resp.json()["gatekeeper_enabled"] is True
    assert resp.json()["gatekeeper_threshold"] == 50
