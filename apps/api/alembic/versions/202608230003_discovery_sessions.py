"""historical buyer-reported discovery sessions

Revision ID: 202608230003
Revises: 202608230002
Create Date: 2026-08-23
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202608230003"
down_revision: str | None = "202608230002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "discovery_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "contact_id",
            sa.Integer(),
            sa.ForeignKey("contacts.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "opportunity_id",
            sa.Integer(),
            sa.ForeignKey("opportunities.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("hypothesis", sa.String(length=60), nullable=False),
        sa.Column("workflow_discussed", sa.Text(), nullable=False),
        sa.Column("discovery_status", sa.String(length=60), nullable=False),
        sa.Column("qualification_outcome", sa.String(length=60), nullable=False),
        sa.Column(
            "evidence_type",
            sa.String(length=30),
            nullable=False,
            server_default="BUYER_REPORTED",
        ),
        sa.Column("existing_software", sa.JSON(), nullable=False),
        sa.Column("buyer_reported_facts", sa.JSON(), nullable=False),
        sa.Column("buyer_reported_metrics", sa.JSON(), nullable=False),
        sa.Column("calculated_metrics", sa.JSON(), nullable=False),
        sa.Column("pain_examples", sa.JSON(), nullable=False),
        sa.Column("objections", sa.JSON(), nullable=False),
        sa.Column("alternatives", sa.JSON(), nullable=False),
        sa.Column("existing_stack_capability", sa.String(length=60), nullable=False),
        sa.Column("qualification", sa.JSON(), nullable=False),
        sa.Column("readiness", sa.JSON(), nullable=False),
        sa.Column("readiness_total", sa.Integer(), nullable=False),
        sa.Column("fatal_blockers", sa.JSON(), nullable=False),
        sa.Column("unresolved_questions", sa.JSON(), nullable=False),
        sa.Column("missing_information", sa.JSON(), nullable=False),
        sa.Column("next_action", sa.Text(), nullable=False),
        sa.Column("raw_notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_discovery_sessions_company_id", "discovery_sessions", ["company_id"])
    op.create_index("ix_discovery_sessions_occurred_at", "discovery_sessions", ["occurred_at"])


def downgrade() -> None:
    op.drop_index("ix_discovery_sessions_occurred_at", table_name="discovery_sessions")
    op.drop_index("ix_discovery_sessions_company_id", table_name="discovery_sessions")
    op.drop_table("discovery_sessions")
