import pytest

from app.services.security import assert_supported_source, extract_youtube_video_id


def test_accepts_youtube_watch_url():
    assert_supported_source("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


def test_rejects_unsupported_host():
    with pytest.raises(ValueError):
        assert_supported_source("https://example.com/watch?v=dQw4w9WgXcQ")


def test_extracts_watch_video_id():
    assert extract_youtube_video_id("https://www.youtube.com/watch?v=abc123") == "abc123"


def test_extracts_short_url_video_id():
    assert extract_youtube_video_id("https://youtu.be/abc123") == "abc123"
