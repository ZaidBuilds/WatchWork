import logging
import threading
import time
from uuid import UUID

import httpx
from sqlmodel import Session, select

from ..database import engine
from ..events import Event, event_bus
from ..models import WebhookConfig

logger = logging.getLogger("action_engine.webhooks")


def _deliver_webhook(url: str, event: Event, attempt: int = 1, max_attempts: int = 3) -> None:
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                url,
                json={
                    "event": event.name,
                    "data": event.data,
                    "timestamp": event.timestamp.isoformat(),
                },
            )
            if 200 <= response.status_code < 300:
                logger.info("Webhook delivered to %s (event=%s, attempt=%d)", url, event.name, attempt)
            elif attempt < max_attempts:
                delay = 2 ** attempt
                logger.warning("Webhook failed (status=%d), retrying attempt %d/%d in %ds", response.status_code, attempt + 1, max_attempts, delay)
                time.sleep(delay)
                _deliver_webhook(url, event, attempt + 1, max_attempts)
            else:
                logger.error("Webhook delivery failed after %d attempts to %s", max_attempts, url)
    except Exception as exc:
        if attempt < max_attempts:
            delay = 2 ** attempt
            logger.warning("Webhook error (%s), retrying attempt %d/%d in %ds", exc, attempt + 1, max_attempts, delay)
            time.sleep(delay)
            _deliver_webhook(url, event, attempt + 1, max_attempts)
        else:
            logger.error("Webhook delivery failed after %d attempts to %s: %s", max_attempts, url, exc)


def _on_event(event: Event) -> None:
    user_id = event.data.get("user_id")
    try:
        with Session(engine) as session:
            query = select(WebhookConfig).where(WebhookConfig.is_active == True)  # noqa: E712
            if user_id:
                query = query.where(WebhookConfig.user_id == UUID(user_id))
            configs = session.exec(query).all()
    except Exception:
        return

    for config in configs:
        if not config.events or event.name in config.events or "*" in config.events:
            threading.Thread(target=_deliver_webhook, args=(config.url, event), daemon=True).start()


event_bus.subscribe("*", _on_event)
