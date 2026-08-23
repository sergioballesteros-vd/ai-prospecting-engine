import json
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.application.opportunity_review import default_opportunity
from app.application.pipeline import current_pipeline_state, transition_pipeline
from app.domain.models import CommercialNote, Company, Contact, Opportunity, PipelineEvent
from app.domain.schemas import (
    CommercialActionCreate,
    CommercialProspectRead,
    ContactUpsert,
    OutreachTemplateRead,
)

COMMERCIAL_ACTIONS = {
    "MARK_CONNECTION_SENT",
    "MARK_ACCEPTED",
    "MARK_REPLIED",
    "MARK_MEETING",
    "MARK_REJECTED",
    "MARK_NO_RESPONSE",
    "ADD_NOTE",
}
TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "data" / "outreach_templates.json"


def list_commercial_prospects(db: Session) -> list[CommercialProspectRead]:
    companies = list(
        db.scalars(
            select(Company)
            .where(
                or_(
                    Company.opportunity_scores.any(),
                    Company.contacts.any(),
                    Company.pipeline_events.any(),
                    Company.commercial_notes.any(),
                    Company.discovery_sessions.any(),
                )
            )
            .options(*_commercial_loaders())
            .order_by(Company.name.asc())
            .execution_options(populate_existing=True)
        )
        .unique()
        .all()
    )
    fallback_opportunity = default_opportunity(db)
    rows = [_commercial_prospect(company, fallback_opportunity) for company in companies]
    return sorted(
        rows,
        key=lambda row: (
            _status_order(row.status),
            -(row.first_customer_fit.total_score if row.first_customer_fit else -1),
            row.company.name.lower(),
        ),
    )


def get_commercial_prospect(db: Session, company_id: int) -> CommercialProspectRead:
    company = db.scalar(
        select(Company)
        .where(Company.id == company_id)
        .options(*_commercial_loaders())
        .execution_options(populate_existing=True)
    )
    if company is None:
        raise ValueError("Company not found")
    return _commercial_prospect(company, default_opportunity(db))


def upsert_primary_contact(db: Session, company_id: int, payload: ContactUpsert) -> Contact:
    company = db.get(Company, company_id)
    if company is None:
        raise ValueError("Company not found")
    if not (payload.full_name or payload.role):
        raise ValueError("Buyer name or role is required")
    contacts = list(db.scalars(select(Contact).where(Contact.company_id == company_id)))
    contact = next((item for item in contacts if item.is_primary), None)
    if contact is None:
        contact = Contact(company_id=company_id, is_primary=True)
        db.add(contact)
    for item in contacts:
        item.is_primary = False
    contact.full_name = payload.full_name
    contact.role = payload.role
    contact.profile_url = payload.profile_url
    contact.channel = payload.channel
    contact.notes = payload.notes
    contact.is_primary = True
    contact.updated_at = datetime.now(UTC)
    db.commit()
    db.refresh(contact)
    return contact


def record_commercial_action(
    db: Session, company_id: int, payload: CommercialActionCreate
) -> CommercialProspectRead:
    if payload.action not in COMMERCIAL_ACTIONS:
        raise ValueError(f"Invalid commercial action: {payload.action}")
    company = db.get(Company, company_id)
    if company is None:
        raise ValueError("Company not found")
    opportunity = _resolve_opportunity(db, company, payload.opportunity_id)
    state = current_pipeline_state(db, company_id, opportunity.id)
    metadata = _action_metadata(payload)

    if payload.action == "MARK_CONNECTION_SENT":
        if state is None:
            transition_pipeline(
                db,
                company_id=company_id,
                opportunity_id=opportunity.id,
                to_state="APPROVED",
                notes="Approved through manual connection recording.",
                metadata={"action": "MANUAL_APPROVAL"},
            )
            state = "APPROVED"
        if state != "APPROVED":
            raise ValueError(f"Cannot mark connection sent from {state}")
        transition_pipeline(
            db,
            company_id=company_id,
            opportunity_id=opportunity.id,
            to_state="CONNECTION_SENT",
            notes=payload.notes,
            metadata=metadata,
            channel=payload.channel or "LINKEDIN",
            message_used=payload.message_used,
        )
    elif payload.action == "MARK_ACCEPTED":
        _transition_action(db, company_id, opportunity.id, "ACCEPTED", payload, metadata)
    elif payload.action == "MARK_REPLIED":
        _transition_action(db, company_id, opportunity.id, "REPLIED", payload, metadata)
    elif payload.action == "MARK_MEETING":
        _transition_action(db, company_id, opportunity.id, "MEETING", payload, metadata)
    elif payload.action == "MARK_REJECTED":
        lost_reason = payload.lost_reason or payload.notes
        if not lost_reason:
            raise ValueError("Rejected prospects require a reason")
        transition_pipeline(
            db,
            company_id=company_id,
            opportunity_id=opportunity.id,
            to_state="LOST",
            notes=payload.notes,
            metadata=metadata,
            lost_reason=lost_reason,
        )
    else:
        _record_note(db, company, opportunity, payload)

    return get_commercial_prospect(db, company_id)


def list_outreach_templates() -> list[OutreachTemplateRead]:
    payload = json.loads(TEMPLATE_PATH.read_text())
    return [OutreachTemplateRead.model_validate(item) for item in payload]


def _transition_action(
    db: Session,
    company_id: int,
    opportunity_id: int,
    to_state: str,
    payload: CommercialActionCreate,
    metadata: dict,
) -> PipelineEvent:
    return transition_pipeline(
        db,
        company_id=company_id,
        opportunity_id=opportunity_id,
        to_state=to_state,
        notes=payload.notes,
        metadata=metadata,
    )


def _record_note(
    db: Session, company: Company, opportunity: Opportunity, payload: CommercialActionCreate
) -> CommercialNote:
    contact = _primary_contact(company.contacts)
    body = payload.notes
    tags = list(payload.learning_tags)
    if payload.action == "MARK_NO_RESPONSE":
        body = body or "No response recorded after the manual follow-up window."
        tags.append("no_response")
    if not body:
        raise ValueError("A manual note requires text")
    note = CommercialNote(
        company_id=company.id,
        contact_id=contact.id if contact else None,
        opportunity_id=opportunity.id,
        body=body,
        learning_tags=sorted(set(tags)),
        evidence_ids=payload.evidence_ids,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def _resolve_opportunity(
    db: Session, company: Company, opportunity_id: int | None
) -> Opportunity:
    if opportunity_id is not None:
        opportunity = db.get(Opportunity, opportunity_id)
        if opportunity is None:
            raise ValueError("Opportunity not found")
        return opportunity
    if company.opportunity_scores:
        latest_score = max(company.opportunity_scores, key=lambda item: item.id)
        opportunity = db.get(Opportunity, latest_score.opportunity_id)
        if opportunity is not None:
            return opportunity
    return default_opportunity(db)


def _action_metadata(payload: CommercialActionCreate) -> dict:
    note_type = None
    if payload.with_note is not None:
        note_type = "WITH_NOTE" if payload.with_note else "WITHOUT_NOTE"
    return {
        "action": payload.action,
        "connection_note_type": note_type,
        "message_version": payload.message_version,
        "evidence_ids": payload.evidence_ids,
        "outreach_reason": payload.outreach_reason,
        "learning_tags": sorted(set(payload.learning_tags)),
    }


def _commercial_loaders():
    return (
        selectinload(Company.contacts),
        selectinload(Company.commercial_notes),
        selectinload(Company.discovery_sessions),
        selectinload(Company.pipeline_events),
        selectinload(Company.opportunity_scores),
        selectinload(Company.first_customer_fit_scores),
        selectinload(Company.evidence),
    )


def _commercial_prospect(
    company: Company, fallback_opportunity: Opportunity
) -> CommercialProspectRead:
    events = sorted(company.pipeline_events, key=lambda item: (item.timestamp, item.id))
    notes = sorted(company.commercial_notes, key=lambda item: (item.created_at, item.id))
    discovery_sessions = sorted(
        company.discovery_sessions,
        key=lambda item: (item.occurred_at, item.id),
        reverse=True,
    )
    latest_event = events[-1] if events else None
    score = max(company.opportunity_scores, key=lambda item: item.id, default=None)
    fit = max(company.first_customer_fit_scores, key=lambda item: item.id, default=None)
    opportunity_id = (
        score.opportunity_id
        if score
        else latest_event.opportunity_id
        if latest_event
        else fallback_opportunity.id
    )
    connection_event = next(
        (item for item in events if item.to_state in {"CONTACTED", "CONNECTION_SENT"}), None
    )
    selected_ids = _selected_evidence_ids(connection_event, fit, score)
    evidence_by_id = {item.id: item for item in company.evidence}
    last_action, last_action_at = _last_action(events, notes)
    raw_state = latest_event.to_state if latest_event else None
    status = _commercial_status(raw_state)
    return CommercialProspectRead(
        company=company,
        opportunity_id=opportunity_id,
        buyer=_primary_contact(company.contacts),
        status=status,
        channel=connection_event.channel if connection_event else None,
        connection_note_used=connection_event.message_used if connection_event else None,
        connection_note_type=_metadata_value(connection_event, "connection_note_type"),
        message_version=_metadata_value(connection_event, "message_version"),
        selected_evidence=[
            evidence_by_id[item_id] for item_id in selected_ids if item_id in evidence_by_id
        ],
        outreach_reason=_outreach_reason(connection_event, fit, score),
        first_customer_fit=fit,
        last_action=last_action,
        last_action_at=last_action_at,
        next_action=_next_action(status),
        contacted_at=_milestone_time(events, {"CONTACTED", "CONNECTION_SENT"}, True),
        accepted_at=_milestone_time(events, {"ACCEPTED"}),
        replied_at=_milestone_time(events, {"REPLIED"}),
        meeting_at=_milestone_time(events, {"MEETING"}),
        proposal_at=_milestone_time(events, {"PROPOSAL"}),
        closed_at=_milestone_time(events, {"WON", "LOST"}),
        lost_reason=_lost_reason(events),
        learning_tags=_learning_tags(events, notes),
        manual_notes=list(reversed(notes)),
        discovery_sessions=discovery_sessions,
    )


def _primary_contact(contacts: list[Contact]) -> Contact | None:
    return max(contacts, key=lambda item: (item.is_primary, item.id), default=None)


def _selected_evidence_ids(connection_event, fit, score) -> list[int]:
    if connection_event:
        values = connection_event.event_metadata.get("evidence_ids", [])
        if isinstance(values, list) and values:
            return [int(item) for item in values]
    if fit:
        return list(fit.evidence_ids)
    return list(score.evidence_ids) if score else []


def _outreach_reason(connection_event, fit, score) -> str | None:
    if connection_event:
        reason = connection_event.event_metadata.get("outreach_reason")
        if isinstance(reason, str) and reason:
            return reason
    if fit:
        return fit.explanation
    return score.explanation if score else None


def _metadata_value(event: PipelineEvent | None, key: str) -> str | None:
    if event is None:
        return None
    value = event.event_metadata.get(key)
    return value if isinstance(value, str) and value else None


def _commercial_status(state: str | None) -> str:
    if state in {None, "APPROVED"}:
        return "TO_CONTACT"
    if state == "CONTACTED":
        return "CONNECTION_SENT"
    return state


def _last_action(
    events: list[PipelineEvent], notes: list[CommercialNote]
) -> tuple[str, datetime | None]:
    latest_event = events[-1] if events else None
    latest_note = notes[-1] if notes else None
    if latest_note and (
        latest_event is None or _as_utc(latest_note.created_at) > _as_utc(latest_event.timestamp)
    ):
        return f"Note: {latest_note.body[:120]}", latest_note.created_at
    if latest_event:
        action = latest_event.event_metadata.get("action")
        return str(action or latest_event.to_state), latest_event.timestamp
    return "No commercial action recorded", None


def _milestone_time(
    events: list[PipelineEvent], states: set[str], prefer_contacted_at: bool = False
) -> datetime | None:
    event = next((item for item in events if item.to_state in states), None)
    if event is None:
        return None
    if prefer_contacted_at and event.contacted_at is not None:
        return event.contacted_at
    return event.timestamp


def _lost_reason(events: list[PipelineEvent]) -> str | None:
    event = next((item for item in reversed(events) if item.to_state == "LOST"), None)
    return event.lost_reason if event else None


def _learning_tags(events: list[PipelineEvent], notes: list[CommercialNote]) -> list[str]:
    tags = {tag for note in notes for tag in note.learning_tags}
    for event in events:
        values = event.event_metadata.get("learning_tags", [])
        if isinstance(values, list):
            tags.update(str(item) for item in values)
    return sorted(tags)


def _next_action(status: str) -> str:
    return {
        "TO_CONTACT": "Resolve buyer and send manually after review",
        "CONNECTION_SENT": "Wait for acceptance; follow up manually if appropriate",
        "ACCEPTED": "Send the evidence-backed discovery message manually",
        "REPLIED": "Qualify pain and request a 15-minute discovery call",
        "MEETING": "Record validated pain and decide whether to propose",
        "PROPOSAL": "Follow up on the proposal manually",
        "WON": "Record revenue and delivery next step",
        "LOST": "Keep the reason and learning; do not contact",
    }.get(status, "Review manually")


def _status_order(status: str) -> int:
    order = [
        "TO_CONTACT",
        "CONNECTION_SENT",
        "ACCEPTED",
        "REPLIED",
        "MEETING",
        "PROPOSAL",
        "WON",
        "LOST",
    ]
    return order.index(status) if status in order else len(order)


def _as_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
