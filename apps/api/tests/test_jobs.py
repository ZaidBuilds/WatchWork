from unittest.mock import patch

from sqlmodel import Session

from app.models import Job, JobStatus
from tests.conftest import test_engine

VALID_YOUTUBE_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def _mock_submit_job(content_item_id, user_id):
    with Session(test_engine) as s:
        job = Job(user_id=user_id, content_item_id=content_item_id)
        s.add(job)
        s.commit()
        s.refresh(job)
        return job


def _mock_get_job_status(job_id):
    with Session(test_engine) as s:
        return s.get(Job, job_id)


def test_process_content(client, user_headers):
    create = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": VALID_YOUTUBE_URL, "platform": "youtube"},
        headers=user_headers,
    )
    content_id = create.json()["id"]

    with patch("app.routers.jobs.submit_job", side_effect=_mock_submit_job):
        resp = client.post(f"/api/content/{content_id}/process", headers=user_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "pending"
    assert data["content_item_id"] == content_id


def test_process_content_not_found(client, user_headers):
    resp = client.post(
        "/api/content/00000000-0000-0000-0000-000000000000/process",
        headers=user_headers,
    )
    assert resp.status_code == 404


def test_process_content_not_owner(client, user_headers, second_user_headers):
    create = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": VALID_YOUTUBE_URL, "platform": "youtube"},
        headers=user_headers,
    )
    content_id = create.json()["id"]
    resp = client.post(
        f"/api/content/{content_id}/process",
        headers=second_user_headers,
    )
    assert resp.status_code == 403


def test_get_job_status(client, user_headers):
    create = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": VALID_YOUTUBE_URL, "platform": "youtube"},
        headers=user_headers,
    )
    content_id = create.json()["id"]

    with patch("app.routers.jobs.submit_job", side_effect=_mock_submit_job):
        process = client.post(f"/api/content/{content_id}/process", headers=user_headers)
    job_id = process.json()["id"]

    with patch("app.routers.jobs.get_job_status", side_effect=_mock_get_job_status):
        resp = client.get(f"/api/jobs/{job_id}", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == job_id


def test_get_job_not_found(client, user_headers):
    with patch("app.routers.jobs.get_job_status", return_value=None):
        resp = client.get(
            "/api/jobs/00000000-0000-0000-0000-000000000000",
            headers=user_headers,
        )
    assert resp.status_code == 404


def test_get_job_not_owner(client, user_headers, second_user_headers):
    create = client.post(
        "/api/ingest/browser-capture",
        json={"source_url": VALID_YOUTUBE_URL, "platform": "youtube"},
        headers=user_headers,
    )
    content_id = create.json()["id"]

    with patch("app.routers.jobs.submit_job", side_effect=_mock_submit_job):
        process = client.post(f"/api/content/{content_id}/process", headers=user_headers)
    job_id = process.json()["id"]

    with patch("app.routers.jobs.get_job_status", side_effect=_mock_get_job_status):
        resp = client.get(f"/api/jobs/{job_id}", headers=second_user_headers)
    assert resp.status_code == 403
