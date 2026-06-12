from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ..database import get_session
from ..deps import get_current_user
from ..models import User, WebhookConfig

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


class WebhookCreateRequest(BaseModel):
    url: str
    events: list[str] = ["*"]


class WebhookResponse(BaseModel):
    id: UUID
    url: str
    events: list[str]
    is_active: bool


@router.get("", response_model=list[WebhookResponse])
def list_webhooks(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return session.exec(select(WebhookConfig).where(WebhookConfig.user_id == user.id)).all()


@router.post("", response_model=WebhookResponse, status_code=201)
def create_webhook(
    payload: WebhookCreateRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    config = WebhookConfig(user_id=user.id, url=payload.url, events=payload.events)
    session.add(config)
    session.commit()
    session.refresh(config)
    return config


@router.delete("/{webhook_id}", status_code=204)
def delete_webhook(
    webhook_id: UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    config = session.get(WebhookConfig, webhook_id)
    if not config or config.user_id != user.id:
        raise HTTPException(status_code=404, detail="Webhook not found.")
    session.delete(config)
    session.commit()
