from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..database import get_session
from ..deps import get_current_user
from ..events import event_bus
from ..models import ActionPlan, Task, User
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
    set_task_done(task, payload.is_done)
    session.add(task)
    completion_pct = recalculate_plan_progress(session, task.action_plan_id)
    session.commit()
    session.refresh(task)

    if payload.is_done:
        event_bus.task_completed(task_id=task.id, plan_id=task.action_plan_id, completion_pct=completion_pct)

    return task
