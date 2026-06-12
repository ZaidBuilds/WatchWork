def test_register_success(client):
    resp = client.post(
        "/api/auth/register",
        json={"email": "new@example.com", "password": "secret123", "name": "New User"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == "new@example.com"
    assert data["name"] == "New User"


def test_register_duplicate_email(client, user_headers):
    resp = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    assert resp.status_code == 409
    assert "already" in resp.json()["detail"].lower()


def test_register_invalid_email(client):
    resp = client.post(
        "/api/auth/register",
        json={"email": "not-an-email", "password": "secret123"},
    )
    assert resp.status_code == 422


def test_login_success(client, user_headers):
    resp = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["email"] == "test@example.com"


def test_login_wrong_password(client, user_headers):
    resp = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "wrongpass"},
    )
    assert resp.status_code == 401


def test_login_nonexistent_user(client):
    resp = client.post(
        "/api/auth/login",
        json={"email": "nobody@example.com", "password": "secret123"},
    )
    assert resp.status_code == 401
