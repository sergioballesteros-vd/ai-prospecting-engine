"""structured discovery workflow details

Revision ID: 202608230004
Revises: 202608230003
Create Date: 2026-08-23
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202608230004"
down_revision: str | None = "202608230003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "discovery_sessions",
        sa.Column("workflow_details", sa.JSON(), nullable=False, server_default="{}"),
    )


def downgrade() -> None:
    op.drop_column("discovery_sessions", "workflow_details")
