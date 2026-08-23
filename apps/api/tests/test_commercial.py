from datetime import UTC, datetime
from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine, func, inspect, select
from sqlalchemy.orm import Session, sessionmaker

from alembic import command
from app.application.commercial import (
    list_outreach_templates,
    record_commercial_action,
    upsert_primary_contact,
)
from app.application.commercial_seed import seed_current_commercial_state
from app.application.discovery import (
    assess_discovery,
    calculate_discovery_metrics,
    create_discovery_session,
)
from app.domain.models import (
    Base,
    CommercialNote,
    Company,
    Contact,
    DiscoverySession,
    Opportunity,
    PipelineEvent,
)
from app.domain.schemas import (
    CommercialActionCreate,
    ContactUpsert,
    DiscoverySessionCreate,
    DiscoverySessionRead,
)
from app.infrastructure.settings import get_settings


def test_manual_first_contact_workflow_preserves_metadata_and_milestones() -> None:
    db = _session()
    company, _ = _context(db)
    buyer = upsert_primary_contact(
        db,
        company.id,
        ContactUpsert(
            full_name="Buyer Name",
            role="Managing Partner",
            profile_url="https://www.linkedin.com/in/example",
        ),
    )

    sent = record_commercial_action(
        db,
        company.id,
        CommercialActionCreate(
            action="MARK_CONNECTION_SENT",
            with_note=True,
            message_used="Manual evidence-backed note",
            message_version="connection-v1",
            evidence_ids=[],
            outreach_reason="Public contact flow",
        ),
    )
    accepted = record_commercial_action(
        db, company.id, CommercialActionCreate(action="MARK_ACCEPTED")
    )
    replied = record_commercial_action(
        db, company.id, CommercialActionCreate(action="MARK_REPLIED")
    )
    meeting = record_commercial_action(
        db, company.id, CommercialActionCreate(action="MARK_MEETING")
    )

    assert buyer.is_primary is True
    assert sent.status == "CONNECTION_SENT"
    assert sent.connection_note_type == "WITH_NOTE"
    assert sent.connection_note_used == "Manual evidence-backed note"
    assert sent.message_version == "connection-v1"
    assert sent.contacted_at is not None
    assert accepted.accepted_at is not None
    assert replied.replied_at is not None
    assert meeting.meeting_at is not None


def test_no_response_and_learning_notes_do_not_change_pipeline_state() -> None:
    db = _session()
    company, _ = _context(db)
    sent = record_commercial_action(
        db, company.id, CommercialActionCreate(action="MARK_CONNECTION_SENT", with_note=False)
    )

    updated = record_commercial_action(
        db,
        company.id,
        CommercialActionCreate(
            action="MARK_NO_RESPONSE",
            notes="Checked manually; no response yet.",
            learning_tags=["buyer_inaccessible"],
        ),
    )

    assert sent.status == "CONNECTION_SENT"
    assert updated.status == "CONNECTION_SENT"
    assert set(updated.learning_tags) == {"buyer_inaccessible", "no_response"}
    assert updated.manual_notes[0].body == "Checked manually; no response yet."


def test_rejection_from_to_contact_requires_and_preserves_reason() -> None:
    db = _session()
    company, _ = _context(db)

    rejected = record_commercial_action(
        db,
        company.id,
        CommercialActionCreate(
            action="MARK_REJECTED",
            lost_reason="Buyer inaccessible",
            learning_tags=["buyer_inaccessible"],
        ),
    )

    assert rejected.status == "LOST"
    assert rejected.lost_reason == "Buyer inaccessible"
    assert rejected.learning_tags == ["buyer_inaccessible"]


def test_current_commercial_seed_is_idempotent() -> None:
    db = _session()
    db.add(_opportunity())
    db.commit()

    first = seed_current_commercial_state(db)
    second = seed_current_commercial_state(db)

    assert first == {"companies": 9, "contacts": 7, "events": 12, "notes": 2}
    assert second == {"companies": 0, "contacts": 0, "events": 0, "notes": 0}
    assert db.scalar(select(func.count()).select_from(Company)) == 9
    assert db.scalar(select(func.count()).select_from(Contact)) == 7
    assert db.scalar(select(func.count()).select_from(PipelineEvent)) == 12
    assert db.scalar(select(func.count()).select_from(CommercialNote)) == 2


def test_templates_are_manual_and_connection_note_structure_is_bounded() -> None:
    templates = list_outreach_templates()
    connection = next(item for item in templates if item.key == "linkedin_connection_note")

    assert all(item.automated is False for item in templates)
    assert connection.max_length == 190
    assert len(connection.body) <= connection.max_length
    assert "evidence_observation" in connection.placeholders


def test_discovery_sessions_preserve_history_and_buyer_reported_evidence() -> None:
    db = _session()
    company, opportunity = _context(db)
    first = create_discovery_session(db, company.id, _discovery_payload(opportunity.id))
    second_payload = _discovery_payload(opportunity.id)
    second_payload.raw_notes = "Second call: buyer supplied a more recent baseline."
    second = create_discovery_session(db, company.id, second_payload)

    sessions = list(
        db.scalars(select(DiscoverySession).order_by(DiscoverySession.id.asc())).all()
    )
    assert [item.id for item in sessions] == [first.id, second.id]
    assert sessions[0].raw_notes == "Verbatim notes"
    assert sessions[0].evidence_type == "BUYER_REPORTED"
    assert sessions[0].buyer_reported_facts == ["Buyer described the last monthly close."]


def test_calculations_use_only_provided_numbers_and_missing_is_not_zero() -> None:
    assert calculate_discovery_metrics({}) == {}

    calculated = calculate_discovery_metrics(
        {"manual_reminders": 12, "minutes_per_reminder": 5, "buyer_hourly_cost": 30}
    )
    assert calculated["derived_total_followup_minutes"]["value"] == 60
    assert calculated["manual_followup_hours"]["value"] == 1
    assert calculated["estimated_monthly_followup_cost"]["value"] == 30

    provided_zero = calculate_discovery_metrics(
        {"manual_reminders": 0, "minutes_per_reminder": 5}
    )
    assert provided_zero["manual_followup_hours"]["value"] == 0


def test_fatal_blockers_override_readiness_total() -> None:
    payload = _discovery_payload()
    payload.qualification.unsafe_requirement = True
    assessment = assess_discovery(payload)

    assert assessment["readiness_total"] == 20
    assert assessment["qualification_outcome"] == "DISQUALIFIED"
    assert "UNSAFE_REQUIREMENT" in assessment["fatal_blockers"]


def test_existing_stack_solved_is_a_successful_discovery_result() -> None:
    payload = _discovery_payload()
    payload.existing_stack_capability = "SOLVES_WITH_REASONABLE_CONFIGURATION"
    payload.qualification.existing_stack_solves = True

    assessment = assess_discovery(payload)

    assert assessment["qualification_outcome"] == "EXISTING_STACK_SOLVES_IT"
    assert "EXISTING_STACK_SOLVES_IT" in assessment["fatal_blockers"]


def test_no_baseline_produces_measure_first() -> None:
    payload = _discovery_payload()
    payload.qualification.usable_baseline = False

    assessment = assess_discovery(payload)

    assert assessment["qualification_outcome"] == "MEASURE_FIRST"
    assert "NO_USABLE_BASELINE" in assessment["fatal_blockers"]


def test_pilot_candidate_requires_sponsor_owner_and_bounded_safe_scope() -> None:
    payload = _discovery_payload()
    payload.qualification.sponsor_confirmed = False
    assert assess_discovery(payload)["qualification_outcome"] == "LABOR_CLOSE_CANDIDATE"

    payload.qualification.sponsor_confirmed = True
    payload.qualification.workflow_owner_confirmed = False
    assert assess_discovery(payload)["qualification_outcome"] == "LABOR_CLOSE_CANDIDATE"

    payload.qualification.workflow_owner_confirmed = True
    payload.qualification.bounded_safe_pilot = True
    assert assess_discovery(payload)["qualification_outcome"] == "PILOT_CANDIDATE"


def test_out_of_scope_candidate_requires_buyer_reported_example() -> None:
    payload = _discovery_payload()
    payload.hypothesis = "OUT_OF_SCOPE_WORK"
    payload.qualification.out_of_scope_example_confirmed = None
    assert assess_discovery(payload)["qualification_outcome"] == "MEASURE_FIRST"

    payload.qualification.out_of_scope_example_confirmed = True
    payload.qualification.sponsor_confirmed = False
    assert assess_discovery(payload)["qualification_outcome"] == "OUT_OF_SCOPE_WORK_CANDIDATE"


def test_discovery_session_serialization_is_stable() -> None:
    db = _session()
    company, opportunity = _context(db)
    session = create_discovery_session(db, company.id, _discovery_payload(opportunity.id))

    serialized = DiscoverySessionRead.model_validate(session).model_dump(mode="json")

    assert serialized["evidence_type"] == "BUYER_REPORTED"
    assert serialized["qualification_outcome"] == "PILOT_CANDIDATE"
    assert serialized["buyer_reported_metrics"]["manual_reminders"] == 12
    assert serialized["workflow_details"]["exception_owner"] == "Payroll lead"
    assert serialized["calculated_metrics"]["manual_followup_hours"]["value"] == 1


def test_migrations_are_idempotent(tmp_path, monkeypatch) -> None:
    database_path = tmp_path / "discovery-migrations.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    get_settings.cache_clear()
    config = Config(str(Path(__file__).parents[1] / "alembic.ini"))

    command.upgrade(config, "head")
    command.upgrade(config, "head")

    engine = create_engine(f"sqlite:///{database_path}")
    assert "discovery_sessions" in inspect(engine).get_table_names()
    get_settings.cache_clear()


def _session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)()


def _context(db: Session) -> tuple[Company, Opportunity]:
    opportunity = _opportunity()
    company = Company(
        name="Example Advisors",
        domain="example-advisors.test",
        website_url="https://example-advisors.test",
        country="Spain",
        city="Madrid",
    )
    db.add_all([opportunity, company])
    db.commit()
    return company, opportunity


def _opportunity() -> Opportunity:
    return Opportunity(
        name="Sales Operations Automation",
        market={"country": "Spain", "industries": ["professional_services"]},
        desired_signals=[],
        excluded_industries=[],
        weights={"icp": 0.3, "pain": 0.3, "value": 0.2, "intent": 0.1, "reachability": 0.1},
    )


def _discovery_payload(opportunity_id: int | None = None) -> DiscoverySessionCreate:
    dimension = {"score": 2, "reason": "Confirmed by the buyer in the last occurrence."}
    return DiscoverySessionCreate(
        opportunity_id=opportunity_id,
        occurred_at=datetime.now(UTC),
        hypothesis="PAYROLL_CLOSE_EXCEPTIONS",
        workflow_discussed="Monthly payroll-close exception control",
        discovery_status="COMPLETED",
        existing_software=["A3"],
        workflow_details={
            "cutoff": "Day 25 at 12:00",
            "portal": "A3 portal",
            "real_client_channels": ["portal", "email"],
            "spreadsheets_side_systems": ["exception tracker"],
            "exception_owner": "Payroll lead",
            "status_visibility_method": "A3 plus exception tracker",
        },
        buyer_reported_facts=["Buyer described the last monthly close."],
        buyer_reported_metrics={
            "client_companies_payroll": 40,
            "companies_requiring_reminders": 8,
            "manual_reminders": 12,
            "minutes_per_reminder": 5,
            "corrections_reopens_last_quarter": 3,
            "buyer_hourly_cost": 30,
        },
        pain_examples=["A late change required a payroll reopen."],
        objections=["A3 may already support part of this."],
        alternatives=["Configure the existing portal first."],
        existing_stack_capability="ADOPTION_GAP",
        qualification={
            "recurring_problem": True,
            "usable_baseline": True,
            "existing_stack_solves": False,
            "sponsor_confirmed": True,
            "workflow_owner_confirmed": True,
            "bounded_safe_pilot": True,
            "unsafe_requirement": False,
            "out_of_scope_example_confirmed": None,
        },
        readiness={
            "pain_frequency": dimension,
            "measurable_baseline": dimension,
            "operational_consequence": dimension,
            "existing_stack_gap": dimension,
            "buyer_authority": dimension,
            "workflow_owner_participation": dimension,
            "implementation_simplicity": dimension,
            "willingness_to_change": dimension,
            "pilot_safety": dimension,
            "repeatability": dimension,
        },
        unresolved_questions=["Confirm portal adoption by cohort."],
        next_action="Review one real close with the workflow owner.",
        raw_notes="Verbatim notes",
    )
