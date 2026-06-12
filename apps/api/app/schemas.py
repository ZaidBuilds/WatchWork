from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class BrowserCaptureRequest(BaseModel):
    platform: str = "youtube"
    source_url: HttpUrl
    title: str | None = None
    channel_name: str | None = None
    thumbnail_url: HttpUrl | None = None
    captured_at: datetime | None = None


class ContentResponse(BaseModel):
    id: UUID
    platform: str
    source_url: str
    title: str | None
    channel_name: str | None
    thumbnail_url: str | None
    status: str
    error_message: str | None
    created_at: datetime


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    category: str
    priority: str
    estimated_minutes: int | None
    is_done: bool


class PlanResponse(BaseModel):
    id: UUID
    summary: str
    key_concepts: list[str]
    completion_pct: int
    tasks: list[TaskResponse]


class ContentDetailResponse(ContentResponse):
    transcript_preview: str | None = None
    plan: PlanResponse | None = None


class UpdateTaskRequest(BaseModel):
    is_done: bool


class SettingsResponse(BaseModel):
    gatekeeper_enabled: bool
    gatekeeper_threshold: int


class UpdateSettingsRequest(BaseModel):
    gatekeeper_enabled: bool
    gatekeeper_threshold: int = Field(ge=10, le=100)


class JobResponse(BaseModel):
    id: UUID
    content_item_id: UUID
    status: str
    result: str | None
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None


class PaginatedResponse(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    items: list
    total: int
    offset: int
    limit: int
