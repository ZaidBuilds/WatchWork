from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel import Session

from ..database import get_session
from ..deps import get_current_user
from ..models import ContentItem, Job, User
from ..schemas import JobResponse
from ..worker import get_job_status, submit_job

router = APIRouter(prefix="/api", tags=["jobs"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/content/{content_id}/process", response_model=JobResponse)
@limiter.limit("5/minute")
def process_content(
    request: Request,
    content_id: UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    item = session.get(ContentItem, content_id)
    if not item:
        raise HTTPException(status_code=404, detail="Content item not found.")
    if item.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to process this content.")

    job = submit_job(content_item_id=content_id, user_id=user.id)
    return job


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(
    job_id: UUID,
    user: User = Depends(get_current_user),
):
    job = get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this job.")
    return job
