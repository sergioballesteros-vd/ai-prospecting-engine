"""first customer fit scores

Revision ID: 202608230001
Revises: 202608170002
Create Date: 2026-08-23
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202608230001"
down_revision: str | None = "202608170002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "first_customer_fit_scores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("size_fit", sa.Float(), nullable=False),
        sa.Column("buyer_accessibility", sa.Float(), nullable=False),
        sa.Column("workflow_fit", sa.Float(), nullable=False),
        sa.Column("automation_gap", sa.Float(), nullable=False),
        sa.Column("sales_simplicity", sa.Float(), nullable=False),
        sa.Column("implementation_fit", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("total_score", sa.Float(), nullable=False),
        sa.Column("positive_reasons", sa.JSON(), nullable=False),
        sa.Column("negative_reasons", sa.JSON(), nullable=False),
        sa.Column("disqualifiers", sa.JSON(), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("matched_signals", sa.JSON(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("company_id", name="uq_first_customer_fit_scores_company"),
    )


def downgrade() -> None:
    op.drop_table("first_customer_fit_scores")
