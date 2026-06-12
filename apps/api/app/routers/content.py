from uuid import UUID

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, col, func, select

from ..config import get_settings
from ..database import get_session
from ..deps import get_current_user
from ..events import event_bus
from ..models import ActionPlan, ContentItem, Task, Transcript, User
from ..schemas import BrowserCaptureRequest, ContentDetailResponse, ContentResponse, PaginatedResponse
from ..services.security import assert_supported_source

router = APIRouter(prefix="/api", tags=["content"])


@router.post("/ingest/browser-capture", response_model=ContentResponse)
def browser_capture(
    payload: BrowserCaptureRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    source_url = str(payload.source_url)

    try:
        assert_supported_source(source_url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    settings = get_settings()
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    daily_count = session.exec(
        select(func.count())
        .select_from(ContentItem)
        .where(ContentItem.user_id == user.id, ContentItem.created_at >= today_start)
    ).one()
    if daily_count >= settings.free_daily_ingest_limit:
        raise HTTPException(
            status_code=429,
            detail=f"Daily capture limit reached ({settings.free_daily_ingest_limit}). Try again tomorrow.",
        )

    blocked_plan = _find_gatekeeper_block(session, user.id)
    if blocked_plan:
        raise HTTPException(
            status_code=409,
            detail=f"Gatekeeper mode is active. Finish the current plan to {user.gatekeeper_threshold}% before adding more content.",
        )

    existing = session.exec(
        select(ContentItem).where(ContentItem.user_id == user.id, ContentItem.source_url == source_url)
    ).first()
    if existing:
        return existing

    item = ContentItem(
        user_id=user.id,
        platform=payload.platform,
        source_url=source_url,
        title=payload.title,
        channel_name=payload.channel_name,
        thumbnail_url=str(payload.thumbnail_url) if payload.thumbnail_url else None,
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    event_bus.content_captured(content_id=item.id, user_id=user.id, title=item.title)
    return item


@router.get("/content")
def list_content(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    total = session.exec(
        select(func.count()).select_from(ContentItem).where(ContentItem.user_id == user.id)
    ).one()
    items = session.exec(
        select(ContentItem)
        .where(ContentItem.user_id == user.id)
        .order_by(col(ContentItem.created_at).desc())
        .offset(offset)
        .limit(limit)
    ).all()
    return PaginatedResponse(items=items, total=total, offset=offset, limit=limit)


@router.get("/content/{content_id}", response_model=ContentDetailResponse)
def get_content(
    content_id: UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    item = session.get(ContentItem, content_id)
    if not item:
        raise HTTPException(status_code=404, detail="Content item not found.")
    if item.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this content.")
    return _content_detail(session, item)


def _find_gatekeeper_block(session: Session, user_id: UUID) -> ActionPlan | None:
    user = session.get(User, user_id)
    if not user or not user.gatekeeper_enabled:
        return None
    items = session.exec(select(ContentItem).where(ContentItem.user_id == user_id)).all()
    item_ids = [item.id for item in items]
    if not item_ids:
        return None
    plans = session.exec(select(ActionPlan).where(ActionPlan.content_item_id.in_(item_ids))).all()
    return next((plan for plan in plans if plan.completion_pct < user.gatekeeper_threshold), None)


def _content_detail(session: Session, item: ContentItem) -> dict:
    transcript = session.exec(select(Transcript).where(Transcript.content_item_id == item.id)).first()
    plan = session.exec(select(ActionPlan).where(ActionPlan.content_item_id == item.id)).first()
    plan_payload = None
    if plan:
        tasks = session.exec(select(Task).where(Task.action_plan_id == plan.id)).all()
        plan_payload = {
            "id": plan.id,
            "summary": plan.summary,
            "key_concepts": plan.key_concepts,
            "completion_pct": plan.completion_pct,
            "tasks": tasks,
        }
    return {
        **item.model_dump(),
        "transcript_preview": transcript.raw_text[:1000] if transcript else None,
        "plan": plan_payload,
    }
