import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable
from uuid import UUID

logger = logging.getLogger("action_engine.events")


@dataclass
class Event:
    name: str
    data: dict[str, Any]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


EventHandler = Callable[[Event], None]


class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[EventHandler]] = {}
        self._lock = threading.Lock()

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        with self._lock:
            self._handlers.setdefault(event_name, []).append(handler)

    def publish(self, event: Event) -> None:
        with self._lock:
            handlers = list(self._handlers.get(event.name, []))
            handlers += list(self._handlers.get("*", []))

        for handler in handlers:
            try:
                handler(event)
            except Exception:
                logger.exception("Event handler error for %s", event.name)

    def content_captured(self, content_id: UUID, user_id: UUID, title: str | None = None) -> None:
        self.publish(Event("content.captured", {"content_id": str(content_id), "user_id": str(user_id), "title": title}))

    def plan_created(self, content_id: UUID, plan_id: UUID, task_count: int, user_id: UUID | None = None) -> None:
        self.publish(Event("plan.created", {"content_id": str(content_id), "plan_id": str(plan_id), "task_count": task_count, "user_id": str(user_id) if user_id else None}))

    def task_completed(self, task_id: UUID, plan_id: UUID, completion_pct: int, user_id: UUID | None = None) -> None:
        self.publish(Event("task.completed", {"task_id": str(task_id), "plan_id": str(plan_id), "completion_pct": completion_pct, "user_id": str(user_id) if user_id else None}))


event_bus = EventBus()
