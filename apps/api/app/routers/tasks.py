from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..database import get_session
from ..deps import get_current_user
from ..events import event_bus
from ..models import ActionPlan, ContentItem, Task, User
from ..schemas import TaskResponse, UpdateTaskRequest
from ..services.progress import recalculate_plan_progress, set_task_done

router = APIRouter(prefix="/api", tags=["tasks"])


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    payload: UpdateTaskRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    plan = session.get(ActionPlan, task.action_plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Action plan not found.")
    item = session.get(ContentItem, plan.content_item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this task.")

    set_task_done(task, payload.is_done)
    session.add(task)
    completion_pct = recalculate_plan_progress(session, task.action_plan_id)
    session.commit()
    session.refresh(task)

    if payload.is_done:
        event_bus.task_completed(task_id=task.id, plan_id=task.action_plan_id, completion_pct=completion_pct, user_id=user.id)

    return task
