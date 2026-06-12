from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ContentStatus(str, Enum):
    pending = "pending"
    transcribing = "transcribing"
    analyzing = "analyzing"
    ready = "ready"
    failed = "failed"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: str | None = None
    hashed_password: str = ""
    subscription_tier: str = "free"
    gatekeeper_enabled: bool = False
    gatekeeper_threshold: int = 70
    created_at: datetime = Field(default_factory=_utcnow)


class ContentItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    platform: str
    source_url: str
    title: str | None = None
    channel_name: str | None = None
    duration_seconds: int | None = None
    thumbnail_url: str | None = None
    status: ContentStatus = ContentStatus.pending
    error_message: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)


class Transcript(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    content_item_id: UUID = Field(foreign_key="contentitem.id", index=True)
    raw_text: str
    language: str = "en"
    source: str = "captions"
    created_at: datetime = Field(default_factory=_utcnow)


class ActionPlan(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    content_item_id: UUID = Field(foreign_key="contentitem.id", index=True)
    summary: str
    key_concepts: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    status: str = "approved"
    completion_pct: int = 0
    created_at: datetime = Field(default_factory=_utcnow)


class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    action_plan_id: UUID = Field(foreign_key="actionplan.id", index=True)
    title: str
    description: str | None = None
    category: str = "execution"
    priority: Priority = Priority.medium
    estimated_minutes: int | None = None
    is_done: bool = False
    completed_at: datetime | None = None
    created_at: datetime = Field(default_factory=_utcnow)


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class Job(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    content_item_id: UUID = Field(foreign_key="contentitem.id", index=True)
    status: JobStatus = JobStatus.pending
    result: str | None = None
    error_message: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None


class AgentLog(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    action_plan_id: UUID = Field(foreign_key="actionplan.id", index=True)
    agent_role: str
    iteration: int = 1
    input_summary: str
    output_json: dict = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=_utcnow)


class WebhookConfig(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    url: str
    events: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    is_active: bool = True
    created_at: datetime = Field(default_factory=_utcnow)
