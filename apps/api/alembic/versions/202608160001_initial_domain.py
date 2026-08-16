"""initial domain

Revision ID: 202608160001
Revises:
Create Date: 2026-08-16
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202608160001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("domain", sa.String(length=255), nullable=False, unique=True),
        sa.Column("website_url", sa.String(length=512), nullable=False),
        sa.Column("industry", sa.String(length=120), nullable=True),
        sa.Column("country", sa.String(length=120), nullable=True),
        sa.Column("city", sa.String(length=120), nullable=True),
        sa.Column("employee_estimate", sa.Integer(), nullable=True),
        sa.Column("linkedin_url", sa.String(length=512), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_companies_domain", "companies", ["domain"], unique=True)

    op.create_table(
        "opportunities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("market", sa.JSON(), nullable=False),
        sa.Column("desired_signals", sa.JSON(), nullable=False),
        sa.Column("excluded_industries", sa.JSON(), nullable=False),
        sa.Column("weights", sa.JSON(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )

    op.create_table(
        "company_sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("source_type", sa.String(length=80), nullable=False),
        sa.Column("source_url", sa.String(length=1024), nullable=False),
        sa.Column(
            "retrieved_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("metadata", sa.JSON(), nullable=False),
    )

    op.create_table(
        "evidence",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "source_id",
            sa.Integer(),
            sa.ForeignKey("company_sources.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("signal_type", sa.String(length=120), nullable=False),
        sa.Column("source_url", sa.String(length=1024), nullable=False),
        sa.Column("content_excerpt", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column(
            "detected_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("metadata", sa.JSON(), nullable=False),
    )

    op.create_table(
        "company_signals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("signal_type", sa.String(length=120), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column(
            "evidence_id",
            sa.Integer(),
            sa.ForeignKey("evidence.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )

    op.create_table(
        "company_analyses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("provider", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("observed_signals", sa.JSON(), nullable=False),
        sa.Column("possible_automation_opportunities", sa.JSON(), nullable=False),
        sa.Column("unknowns", sa.JSON(), nullable=False),
        sa.Column("recommended_buyer_roles", sa.JSON(), nullable=False),
        sa.Column("raw_output", sa.JSON(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )

    opportunities = sa.table(
        "opportunities",
        sa.column("name", sa.String),
        sa.column("market", sa.JSON),
        sa.column("desired_signals", sa.JSON),
        sa.column("excluded_industries", sa.JSON),
        sa.column("weights", sa.JSON),
    )
    op.bulk_insert(
        opportunities,
        [
            {
                "name": "Sales Operations Automation",
                "market": {
                    "country": "Spain",
                    "company_size": {"min": 10, "max": 150},
                    "industries": [
                        "real_estate",
                        "insurance",
                        "education",
                        "professional_services",
                        "private_clinics",
                        "b2b_agencies",
                    ],
                },
                "desired_signals": [
                    "HAS_SALES_TEAM",
                    "MULTIPLE_LEAD_CHANNELS",
                    "HAS_CRM",
                    "MULTIPLE_LOCATIONS",
                    "MULTIPLE_CONTACT_FORMS",
                ],
                "excluded_industries": ["energy"],
                "weights": {
                    "icp": 0.30,
                    "pain": 0.30,
                    "value": 0.20,
                    "intent": 0.10,
                    "reachability": 0.10,
                },
            }
        ],
    )


def downgrade() -> None:
    op.drop_table("company_analyses")
    op.drop_table("company_signals")
    op.drop_table("evidence")
    op.drop_table("company_sources")
    op.drop_table("opportunities")
    op.drop_index("ix_companies_domain", table_name="companies")
    op.drop_table("companies")
