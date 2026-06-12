from datetime import datetime, timezone
from uuid import UUID

from sqlmodel import Session, select

from ..models import ActionPlan, Task


def recalculate_plan_progress(session: Session, action_plan_id: UUID) -> int:
    tasks = session.exec(select(Task).where(Task.action_plan_id == action_plan_id)).all()
    completion = 0 if not tasks else round(sum(1 for task in tasks if task.is_done) / len(tasks) * 100)
    plan = session.get(ActionPlan, action_plan_id)
    if plan:
        plan.completion_pct = completion
        session.add(plan)
    return completion


def set_task_done(task: Task, is_done: bool) -> None:
    task.is_done = is_done
    task.completed_at = datetime.now(timezone.utc) if is_done else None
