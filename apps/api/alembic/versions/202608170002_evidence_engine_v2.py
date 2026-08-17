"""evidence engine v2 diagnostics and dedupe

Revision ID: 202608170002
Revises: 202608170001
Create Date: 2026-08-17
"""

import hashlib
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202608170002"
down_revision: str | None = "202608170001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    evidence_columns = {column["name"] for column in inspector.get_columns("evidence")}
    if "fingerprint" not in evidence_columns:
        op.add_column("evidence", sa.Column("fingerprint", sa.String(length=64), nullable=True))
    _backfill_fingerprints(connection)
    with op.batch_alter_table("evidence") as batch_op:
        batch_op.alter_column(
            "fingerprint", existing_type=sa.String(length=64), nullable=False
        )
        constraints = {
            constraint["name"] for constraint in inspector.get_unique_constraints("evidence")
        }
        if "uq_evidence_company_fingerprint" not in constraints:
            batch_op.create_unique_constraint(
                "uq_evidence_company_fingerprint", ["company_id", "fingerprint"]
            )

    research_run_columns = {
        column["name"] for column in inspector.get_columns("research_runs")
    }
    if "diagnostics" not in research_run_columns:
        op.add_column(
            "research_runs",
            sa.Column("diagnostics", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        )
        with op.batch_alter_table("research_runs") as batch_op:
            batch_op.alter_column("diagnostics", server_default=None)


def downgrade() -> None:
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    research_run_columns = {
        column["name"] for column in inspector.get_columns("research_runs")
    }
    if "diagnostics" in research_run_columns:
        with op.batch_alter_table("research_runs") as batch_op:
            batch_op.drop_column("diagnostics")

    evidence_columns = {column["name"] for column in inspector.get_columns("evidence")}
    if "fingerprint" in evidence_columns:
        with op.batch_alter_table("evidence") as batch_op:
            constraints = {
                constraint["name"] for constraint in inspector.get_unique_constraints("evidence")
            }
            if "uq_evidence_company_fingerprint" in constraints:
                batch_op.drop_constraint("uq_evidence_company_fingerprint", type_="unique")
            batch_op.drop_column("fingerprint")


def _backfill_fingerprints(connection) -> None:
    rows = connection.execute(
        sa.text(
            "select id, signal_type, source_url, content_excerpt from evidence "
            "where fingerprint is null"
        )
    ).mappings()
    seen: set[str] = set()
    for row in rows:
        payload = (
            f"{row['signal_type']}|{row['source_url'].strip().lower()}|"
            f"{' '.join(row['content_excerpt'].lower().split())[:500]}"
        )
        fingerprint = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        while fingerprint in seen:
            fingerprint = hashlib.sha256(f"{fingerprint}|{row['id']}".encode()).hexdigest()
        seen.add(fingerprint)
        connection.execute(
            sa.text("update evidence set fingerprint = :fingerprint where id = :id"),
            {"fingerprint": fingerprint, "id": row["id"]},
        )
