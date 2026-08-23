"""align timestamp constraints and commercial indexes with models

Revision ID: 202608230005
Revises: 202608230004
Create Date: 2026-08-23
"""

from collections.abc import Iterable

import sqlalchemy as sa

from alembic import op

revision: str = "202608230005"
down_revision: str | None = "202608230004"
branch_labels: str | None = None
depends_on: str | None = None


TIMESTAMP_COLUMNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("campaign_companies", ("created_at", "updated_at")),
    ("commercial_notes", ("created_at",)),
    ("contacts", ("created_at", "updated_at")),
    ("first_customer_fit_scores", ("created_at", "updated_at")),
    ("opportunity_scores", ("created_at", "updated_at")),
    ("outreach_drafts", ("created_at", "updated_at")),
    ("pipeline_events", ("timestamp",)),
    ("prospecting_campaigns", ("created_at",)),
    ("research_runs", ("created_at",)),
)


def _set_nullable(nullable: bool) -> None:
    bind = op.get_bind()
    for table_name, column_names in TIMESTAMP_COLUMNS:
        if bind.dialect.name == "sqlite":
            with op.batch_alter_table(table_name) as batch_op:
                _alter_columns(batch_op, column_names, nullable)
        else:
            _alter_columns(op, column_names, nullable, table_name=table_name)


def _alter_columns(
    operations: object,
    column_names: Iterable[str],
    nullable: bool,
    *,
    table_name: str | None = None,
) -> None:
    for column_name in column_names:
        kwargs = {
            "existing_type": sa.DateTime(timezone=True),
            "nullable": nullable,
        }
        if table_name is None:
            operations.alter_column(column_name, **kwargs)
        else:
            operations.alter_column(table_name, column_name, **kwargs)


def upgrade() -> None:
    _set_nullable(False)


def downgrade() -> None:
    _set_nullable(True)
