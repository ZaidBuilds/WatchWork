from urllib.parse import urlparse

ALLOWED_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def assert_supported_source(url: str) -> None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host not in ALLOWED_HOSTS:
        raise ValueError("Only YouTube URLs are supported in this MVP.")
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https.")


def extract_youtube_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host == "youtu.be":
        return parsed.path.strip("/") or None
    if parsed.path == "/watch":
        query = dict(part.split("=", 1) for part in parsed.query.split("&") if "=" in part)
        return query.get("v")
    if parsed.path.startswith("/shorts/"):
        return parsed.path.split("/")[2]
    return None
