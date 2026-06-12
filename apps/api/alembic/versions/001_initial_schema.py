"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-12
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("subscription_tier", sa.String(), nullable=False),
        sa.Column("gatekeeper_enabled", sa.Boolean(), nullable=False),
        sa.Column("gatekeeper_threshold", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_email", "user", ["email"], unique=True)

    op.create_table(
        "contentitem",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("platform", sa.String(), nullable=False),
        sa.Column("source_url", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("channel_name", sa.String(), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("thumbnail_url", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("error_message", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_contentitem_user_id", "contentitem", ["user_id"])

    op.create_table(
        "transcript",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("content_item_id", sa.Uuid(), nullable=False),
        sa.Column("raw_text", sa.String(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["content_item_id"], ["contentitem.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_transcript_content_item_id", "transcript", ["content_item_id"])

    op.create_table(
        "actionplan",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("content_item_id", sa.Uuid(), nullable=False),
        sa.Column("summary", sa.String(), nullable=False),
        sa.Column("key_concepts", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("completion_pct", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["content_item_id"], ["contentitem.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_actionplan_content_item_id", "actionplan", ["content_item_id"])

    op.create_table(
        "job",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("content_item_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("result", sa.String(), nullable=True),
        sa.Column("error_message", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["content_item_id"], ["contentitem.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_job_user_id", "job", ["user_id"])
    op.create_index("ix_job_content_item_id", "job", ["content_item_id"])

    op.create_table(
        "task",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("action_plan_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("priority", sa.String(), nullable=False),
        sa.Column("estimated_minutes", sa.Integer(), nullable=True),
        sa.Column("is_done", sa.Boolean(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["action_plan_id"], ["actionplan.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_task_action_plan_id", "task", ["action_plan_id"])

    op.create_table(
        "agentlog",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("action_plan_id", sa.Uuid(), nullable=False),
        sa.Column("agent_role", sa.String(), nullable=False),
        sa.Column("iteration", sa.Integer(), nullable=False),
        sa.Column("input_summary", sa.String(), nullable=False),
        sa.Column("output_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["action_plan_id"], ["actionplan.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agentlog_action_plan_id", "agentlog", ["action_plan_id"])


def downgrade() -> None:
    op.drop_table("agentlog")
    op.drop_table("task")
    op.drop_table("job")
    op.drop_table("actionplan")
    op.drop_table("transcript")
    op.drop_table("contentitem")
    op.drop_table("user")
