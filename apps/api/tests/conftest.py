import os
import atexit
os.environ.setdefault("ALEMBIC_MIGRATIONS_RUN", "1")

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

import app.models  # noqa: F401
import app.main  # noqa: F401

from app.main import app as fastapi_app
from app.database import get_session

TEST_DATABASE_URL = "sqlite:///./test_action_engine.sqlite"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

SQLModel.metadata.create_all(test_engine)


def override_get_session():
    with Session(test_engine) as session:
        yield session


fastapi_app.dependency_overrides[get_session] = override_get_session


@atexit.register
def _cleanup_db():
    try:
        os.unlink("test_action_engine.sqlite")
        os.unlink("test_action_engine.sqlite-wal")
        os.unlink("test_action_engine.sqlite-shm")
    except (FileNotFoundError, PermissionError):
        pass


@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(test_engine)
    yield
    for table in reversed(SQLModel.metadata.sorted_tables):
        with test_engine.connect() as conn:
            conn.execute(table.delete())
            conn.commit()


@pytest.fixture
def client():
    return TestClient(fastapi_app)


@pytest.fixture
def user_headers(client):
    resp = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpass123", "name": "Test User"},
    )
    assert resp.status_code == 201
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def second_user_headers(client):
    resp = client.post(
        "/api/auth/register",
        json={"email": "other@example.com", "password": "otherpass123", "name": "Other User"},
    )
    assert resp.status_code == 201
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_session():
    with Session(test_engine) as session:
        yield session
