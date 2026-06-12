import json

from openai import OpenAI

from ..config import get_settings


FALLBACK_PLAN = {
    "summary": "Transcript captured. Add your OpenAI API key to generate a richer execution plan.",
    "key_concepts": ["Captured transcript", "Manual review needed", "Execution tracking"],
    "tasks": [
        {
            "title": "Review the transcript",
            "description": "Skim the transcript and mark the most useful ideas.",
            "category": "review",
            "priority": "medium",
            "estimated_minutes": 20,
        },
        {
            "title": "Pick one immediate action",
            "description": "Choose one idea from the content and turn it into a small practical task.",
            "category": "execution",
            "priority": "high",
            "estimated_minutes": 30,
        },
    ],
}


PLAN_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["summary", "key_concepts", "tasks"],
    "properties": {
        "summary": {"type": "string"},
        "key_concepts": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 8,
        },
        "tasks": {
            "type": "array",
            "minItems": 2,
            "maxItems": 10,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "description", "category", "priority", "estimated_minutes"],
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "category": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                    "estimated_minutes": {"type": "integer", "minimum": 5, "maximum": 240},
                },
            },
        },
    },
}


def generate_action_plan(title: str | None, transcript: str) -> dict:
    settings = get_settings()
    if not settings.openai_api_key:
        return FALLBACK_PLAN

    client = OpenAI(api_key=settings.openai_api_key)
    transcript_slice = transcript[:18000]
    prompt = (
        "You are Action Engine, an execution-focused planning agent. "
        "Turn this learning content into concrete tasks. Avoid vague tasks. "
        "Every task should be something the user can check off.\n\n"
        f"Title: {title or 'Untitled content'}\n\nTranscript:\n{transcript_slice}"
    )

    response = client.responses.create(
        model=settings.openai_model,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "action_plan",
                "schema": PLAN_SCHEMA,
                "strict": True,
            }
        },
    )
    return json.loads(response.output_text)
