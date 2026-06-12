import logging
import threading
import traceback
from datetime import datetime, timezone
from uuid import UUID

from sqlmodel import Session

from .database import engine
from .events import event_bus
from .models import ActionPlan, AgentLog, ContentItem, ContentStatus, Job, JobStatus, Task, Transcript
from .services.planner import generate_action_plan
from .services.transcripts import fetch_youtube_transcript

logger = logging.getLogger("action_engine.worker")

_jobs_lock = threading.Lock()
_active_jobs: set[UUID] = set()
_worker_thread: threading.Thread | None = None
_stop_event = threading.Event()


def _process_job(job_id: UUID) -> None:
    with Session(engine) as session:
        job = session.get(Job, job_id)
        if not job:
            return

        job.status = JobStatus.running
        job.started_at = datetime.now(timezone.utc)
        session.add(job)
        session.commit()

        item = session.get(ContentItem, job.content_item_id)
        if not item:
            job.status = JobStatus.failed
            job.error_message = "Content item not found."
            job.completed_at = datetime.now(timezone.utc)
            session.add(job)
            session.commit()
            return

        try:
            item.status = ContentStatus.transcribing
            session.add(item)
            session.commit()

            raw_text, language = fetch_youtube_transcript(item.source_url)
            transcript = Transcript(content_item_id=item.id, raw_text=raw_text, language=language)
            session.add(transcript)
            session.commit()

            item.status = ContentStatus.analyzing
            session.add(item)
            session.commit()

            plan_json = generate_action_plan(item.title, raw_text)
            plan = ActionPlan(
                content_item_id=item.id,
                summary=plan_json["summary"],
                key_concepts=plan_json["key_concepts"],
            )
            session.add(plan)
            session.commit()
            session.refresh(plan)

            for task_json in plan_json["tasks"]:
                session.add(
                    Task(
                        action_plan_id=plan.id,
                        title=task_json["title"],
                        description=task_json["description"],
                        category=task_json["category"],
                        priority=task_json["priority"],
                        estimated_minutes=task_json["estimated_minutes"],
                    )
                )
            session.add(
                AgentLog(
                    action_plan_id=plan.id,
                    agent_role="planner",
                    input_summary=f"Transcript characters: {len(raw_text)}",
                    output_json=plan_json,
                )
            )
            item.status = ContentStatus.ready
            item.error_message = None
            session.add(item)

            job.status = JobStatus.completed
            job.result = f"Plan created with {len(plan_json['tasks'])} tasks."
            job.completed_at = datetime.now(timezone.utc)
            session.add(job)
            session.commit()
            logger.info("Job %s completed successfully.", job_id)

            event_bus.plan_created(content_id=item.id, plan_id=plan.id, task_count=len(plan_json["tasks"]), user_id=item.user_id)
        except Exception as exc:
            item.status = ContentStatus.failed
            item.error_message = str(exc)
            session.add(item)

            job.status = JobStatus.failed
            job.error_message = str(exc)
            job.completed_at = datetime.now(timezone.utc)
            session.add(job)
            session.commit()
            logger.error("Job %s failed: %s", job_id, exc)


def _worker_loop() -> None:
    logger.info("Worker thread started.")
    while not _stop_event.is_set():
        job_id = None
        with _jobs_lock:
            if _active_jobs:
                job_id = _active_jobs.pop()
        if job_id:
            _process_job(job_id)
        else:
            _stop_event.wait(timeout=1.0)
    logger.info("Worker thread stopped.")


def _ensure_worker() -> None:
    global _worker_thread
    if _worker_thread is None or not _worker_thread.is_alive():
        _stop_event.clear()
        _worker_thread = threading.Thread(target=_worker_loop, daemon=True)
        _worker_thread.start()


def submit_job(content_item_id: UUID, user_id: UUID) -> Job:
    with Session(engine) as session:
        job = Job(user_id=user_id, content_item_id=content_item_id)
        session.add(job)
        session.commit()
        session.refresh(job)

        with _jobs_lock:
            _active_jobs.add(job.id)

        _ensure_worker()
        return job


def get_job_status(job_id: UUID) -> Job | None:
    with Session(engine) as session:
        return session.get(Job, job_id)
