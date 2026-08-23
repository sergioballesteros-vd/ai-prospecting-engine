from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import Contact, DiscoverySession, Opportunity, PipelineEvent
from app.domain.schemas import (
    CommercialScoreboardRead,
    DiscoverySessionCreate,
)

DISCOVERY_OUTCOMES = {
    "NO_PROBLEM",
    "EXISTING_STACK_SOLVES_IT",
    "MEASURE_FIRST",
    "LABOR_CLOSE_CANDIDATE",
    "OUT_OF_SCOPE_WORK_CANDIDATE",
    "OTHER_WORKFLOW_SIGNAL",
    "PILOT_CANDIDATE",
    "DISQUALIFIED",
}


def calculate_discovery_metrics(metrics: dict) -> dict:
    """Return transparent calculations only when every named input was supplied."""

    calculated: dict[str, dict] = {}
    total_minutes = metrics.get("total_followup_minutes")
    if total_minutes is None:
        reminders = metrics.get("manual_reminders")
        minutes_per_reminder = metrics.get("minutes_per_reminder")
        if reminders is not None and minutes_per_reminder is not None:
            total_minutes = reminders * minutes_per_reminder
            calculated["derived_total_followup_minutes"] = {
                "value": round(total_minutes, 2),
                "unit": "minutes/month",
                "formula": "manual_reminders * minutes_per_reminder",
                "source_fields": ["manual_reminders", "minutes_per_reminder"],
            }

    if total_minutes is not None:
        followup_hours = total_minutes / 60
        calculated["manual_followup_hours"] = {
            "value": round(followup_hours, 2),
            "unit": "hours/month",
            "formula": "total_followup_minutes / 60",
            "source_fields": [
                "total_followup_minutes"
                if metrics.get("total_followup_minutes") is not None
                else "derived_total_followup_minutes"
            ],
        }
        hourly_cost = metrics.get("buyer_hourly_cost")
        if hourly_cost is not None:
            calculated["estimated_monthly_followup_cost"] = {
                "value": round(followup_hours * hourly_cost, 2),
                "unit": "EUR/month",
                "formula": "manual_followup_hours * buyer_hourly_cost",
                "source_fields": ["manual_followup_hours", "buyer_hourly_cost"],
            }

    estimated_value = metrics.get("out_of_scope_estimated_value")
    invoiced_value = metrics.get("out_of_scope_invoiced_value")
    if estimated_value is not None and invoiced_value is not None:
        calculated["potential_absorbed_value"] = {
            "value": round(estimated_value - invoiced_value, 2),
            "unit": "EUR/90d",
            "formula": "out_of_scope_estimated_value - out_of_scope_invoiced_value",
            "source_fields": [
                "out_of_scope_estimated_value",
                "out_of_scope_invoiced_value",
            ],
        }
    return calculated


def assess_discovery(payload: DiscoverySessionCreate) -> dict:
    qualification = payload.qualification
    readiness = payload.readiness.model_dump()
    readiness_total = sum(item["score"] for item in readiness.values())
    fatal_blockers: list[str] = []

    stack_solves = (
        qualification.existing_stack_solves is True
        or payload.existing_stack_capability == "SOLVES_WITH_REASONABLE_CONFIGURATION"
    )
    if stack_solves:
        fatal_blockers.append("EXISTING_STACK_SOLVES_IT")
    if qualification.usable_baseline is not True:
        fatal_blockers.append("NO_USABLE_BASELINE")
    if qualification.sponsor_confirmed is not True:
        fatal_blockers.append("NO_CONFIRMED_SPONSOR")
    if qualification.workflow_owner_confirmed is not True:
        fatal_blockers.append("NO_WORKFLOW_OWNER")
    if qualification.unsafe_requirement:
        fatal_blockers.append("UNSAFE_REQUIREMENT")
    if qualification.recurring_problem is not True:
        fatal_blockers.append("NON_RECURRING_OR_UNCONFIRMED")
    if qualification.bounded_safe_pilot is not True:
        fatal_blockers.append("PILOT_NOT_BOUNDED_SAFE")

    outcome = _qualification_outcome(payload, stack_solves)
    missing_information = _missing_information(payload)
    return {
        "qualification_outcome": outcome,
        "readiness": readiness,
        "readiness_total": readiness_total,
        "fatal_blockers": fatal_blockers,
        "missing_information": missing_information,
    }


def create_discovery_session(
    db: Session, company_id: int, payload: DiscoverySessionCreate
) -> DiscoverySession:
    if payload.contact_id is not None:
        contact = db.get(Contact, payload.contact_id)
        if contact is None or contact.company_id != company_id:
            raise ValueError("Contact does not belong to this prospect")
    if payload.opportunity_id is not None and db.get(Opportunity, payload.opportunity_id) is None:
        raise ValueError("Opportunity not found")

    assessment = assess_discovery(payload)
    buyer_metrics = payload.buyer_reported_metrics.model_dump(exclude_none=True)
    session = DiscoverySession(
        company_id=company_id,
        contact_id=payload.contact_id,
        opportunity_id=payload.opportunity_id,
        occurred_at=payload.occurred_at,
        hypothesis=payload.hypothesis,
        workflow_discussed=payload.workflow_discussed,
        discovery_status=payload.discovery_status,
        qualification_outcome=assessment["qualification_outcome"],
        evidence_type="BUYER_REPORTED",
        existing_software=_clean_list(payload.existing_software),
        workflow_details=payload.workflow_details.model_dump(exclude_none=True),
        buyer_reported_facts=_clean_list(payload.buyer_reported_facts),
        buyer_reported_metrics=buyer_metrics,
        calculated_metrics=calculate_discovery_metrics(buyer_metrics),
        pain_examples=_clean_list(payload.pain_examples),
        objections=_clean_list(payload.objections),
        alternatives=_clean_list(payload.alternatives),
        existing_stack_capability=payload.existing_stack_capability,
        qualification=payload.qualification.model_dump(),
        readiness=assessment["readiness"],
        readiness_total=assessment["readiness_total"],
        fatal_blockers=assessment["fatal_blockers"],
        unresolved_questions=_clean_list(payload.unresolved_questions),
        missing_information=assessment["missing_information"],
        next_action=payload.next_action.strip(),
        raw_notes=payload.raw_notes.strip() if payload.raw_notes else None,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def commercial_scoreboard(db: Session) -> CommercialScoreboardRead:
    events = list(db.scalars(select(PipelineEvent)).all())
    sessions = list(
        db.scalars(
            select(DiscoverySession).order_by(
                DiscoverySession.company_id,
                DiscoverySession.occurred_at.desc(),
                DiscoverySession.id.desc(),
            )
        ).all()
    )
    reached: dict[str, set[int]] = defaultdict(set)
    for event in events:
        reached[event.to_state].add(event.company_id)
    reached["CONNECTION_SENT"].update(reached["CONTACTED"])

    latest_by_company: dict[int, DiscoverySession] = {}
    for session in sessions:
        latest_by_company.setdefault(session.company_id, session)
    outcomes: dict[str, int] = defaultdict(int)
    for session in latest_by_company.values():
        outcomes[session.qualification_outcome] += 1

    won_events = [event for event in events if event.to_state == "WON"]
    return CommercialScoreboardRead(
        connections_sent=len(reached["CONNECTION_SENT"]),
        connections_accepted=len(reached["ACCEPTED"]),
        conversations_started=len(reached["REPLIED"]),
        discovery_calls=len(sessions),
        no_problem=outcomes["NO_PROBLEM"],
        existing_stack_solves_it=outcomes["EXISTING_STACK_SOLVES_IT"],
        measure_first=outcomes["MEASURE_FIRST"],
        payroll_candidates=outcomes["LABOR_CLOSE_CANDIDATE"],
        out_of_scope_candidates=outcomes["OUT_OF_SCOPE_WORK_CANDIDATE"],
        other_workflow_signals=outcomes["OTHER_WORKFLOW_SIGNAL"],
        pilot_candidates=outcomes["PILOT_CANDIDATE"],
        disqualified=outcomes["DISQUALIFIED"],
        pilots_proposed=len(reached["PROPOSAL"]),
        pilots_paid=len(reached["WON"]),
        setup_revenue=round(sum(event.implementation_revenue or 0 for event in won_events), 2),
        mrr=round(sum(event.recurring_revenue_monthly or 0 for event in won_events), 2),
    )


def _qualification_outcome(
    payload: DiscoverySessionCreate, stack_solves: bool
) -> str:
    qualification = payload.qualification
    if qualification.unsafe_requirement:
        return "DISQUALIFIED"
    if qualification.recurring_problem is False:
        return "NO_PROBLEM"
    if stack_solves:
        return "EXISTING_STACK_SOLVES_IT"
    if qualification.recurring_problem is None or qualification.usable_baseline is not True:
        return "MEASURE_FIRST"

    if payload.hypothesis == "OUT_OF_SCOPE_WORK":
        has_buyer_example = bool(payload.buyer_reported_facts or payload.pain_examples)
        if qualification.out_of_scope_example_confirmed is not True or not has_buyer_example:
            return "MEASURE_FIRST"
        candidate = "OUT_OF_SCOPE_WORK_CANDIDATE"
    elif payload.hypothesis == "PAYROLL_CLOSE_EXCEPTIONS":
        candidate = "LABOR_CLOSE_CANDIDATE"
    else:
        candidate = "OTHER_WORKFLOW_SIGNAL"

    pilot_gate = all(
        value is True
        for value in (
            qualification.sponsor_confirmed,
            qualification.workflow_owner_confirmed,
            qualification.bounded_safe_pilot,
        )
    ) and (
        qualification.existing_stack_solves is False
        and payload.existing_stack_capability
        in {"CONFIGURATION_GAP", "ADOPTION_GAP", "FUNCTIONALITY_GAP"}
    )
    return "PILOT_CANDIDATE" if pilot_gate and candidate != "OTHER_WORKFLOW_SIGNAL" else candidate


def _missing_information(payload: DiscoverySessionCreate) -> list[str]:
    missing: list[str] = []
    qualification = payload.qualification
    for field, value in (
        ("recurring_problem", qualification.recurring_problem),
        ("usable_baseline", qualification.usable_baseline),
        ("existing_stack_solves", qualification.existing_stack_solves),
        ("sponsor_confirmed", qualification.sponsor_confirmed),
        ("workflow_owner_confirmed", qualification.workflow_owner_confirmed),
        ("bounded_safe_pilot", qualification.bounded_safe_pilot),
    ):
        if value is None:
            missing.append(field)
    if not payload.existing_software:
        missing.append("existing_software")
    if payload.existing_stack_capability == "UNKNOWN":
        missing.append("existing_stack_capability")

    metrics = payload.buyer_reported_metrics
    if payload.hypothesis == "PAYROLL_CLOSE_EXCEPTIONS":
        for field in (
            "client_companies_payroll",
            "companies_requiring_reminders",
            "manual_reminders",
            "corrections_reopens_last_quarter",
        ):
            if getattr(metrics, field) is None:
                missing.append(field)
    elif payload.hypothesis == "OUT_OF_SCOPE_WORK":
        if metrics.out_of_scope_examples_90d is None:
            missing.append("out_of_scope_examples_90d")
        if qualification.out_of_scope_example_confirmed is None:
            missing.append("out_of_scope_example_confirmed")
    return missing


def _clean_list(values: list[str]) -> list[str]:
    return [value.strip() for value in values if value.strip()]
