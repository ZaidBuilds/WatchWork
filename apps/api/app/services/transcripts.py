from youtube_transcript_api import YouTubeTranscriptApi

from .security import extract_youtube_video_id


def fetch_youtube_transcript(url: str) -> tuple[str, str]:
    video_id = extract_youtube_video_id(url)
    if not video_id:
        raise ValueError("Could not detect a YouTube video id.")

    transcript = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
    lines = [snippet.text.strip() for snippet in transcript if snippet.text.strip()]
    if not lines:
        raise ValueError("No transcript text was found for this video.")
    return "\n".join(lines), "en"
