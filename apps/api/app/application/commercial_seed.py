from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.opportunity_review import default_opportunity
from app.application.pipeline import current_pipeline_state, transition_pipeline
from app.domain.models import CommercialNote, Company, Contact, PipelineEvent
from app.infrastructure.database import SessionLocal

CURRENT_COMMERCIAL_STATE = [
    {
        "key": "ce-consulting-jesus-connection",
        "company": "CE Consulting",
        "domain": "ceconsulting.es",
        "buyer": "Jesús Ignacio",
        "status": "CONNECTION_SENT",
        "note_type": "WITH_NOTE",
        "reason": "Advisory-network and office footprint; test how inbound requests are routed.",
        "city": None,
        "tags": ["local_office_preferred"],
    },
    {
        "key": "aselec-alberto-connection",
        "company": "Aselec Consultores",
        "domain": "aselecconsultores.com",
        "buyer": "Alberto Torrecillas",
        "status": "CONNECTION_SENT",
        "note_type": "WITH_NOTE",
        "reason": "Public contact flow and client-attention hours support a manual triage test.",
        "city": "Murcia",
        "tags": [],
    },
    {
        "key": "gestoria-ds-diego-connection",
        "company": "Gestoría DS",
        "domain": "gestoriadsmadrid.com",
        "buyer": "Diego Domínguez",
        "status": "CONNECTION_SENT",
        "note_type": "WITH_NOTE",
        "reason": "Public contact paths and advisory areas support an intake-routing hypothesis.",
        "city": "Madrid",
        "tags": [],
    },
    {
        "key": "gaudium-marta-connection",
        "company": "Gaudium Asesores",
        "domain": "gaudiumasesores.es",
        "buyer": "Marta Gómez",
        "status": "CONNECTION_SENT",
        "note_type": "WITH_NOTE",
        "reason": "Public document-heavy services support a document-intake and routing test.",
        "city": "Madrid",
        "tags": [],
    },
    {
        "key": "ok-asesores-david-connection",
        "company": "OK Asesores",
        "domain": "okasesores.es",
        "buyer": "David Lahuerta",
        "status": "CONNECTION_SENT",
        "note_type": "WITHOUT_NOTE",
        "reason": "Multiple public contact paths support a lead follow-up hypothesis.",
        "city": "Madrid",
        "tags": [],
    },
    {
        "key": "ayuda-t-pymes-first-fit-rejection",
        "company": "Ayuda T Pymes",
        "domain": "ayudatpymes.com",
        "buyer": None,
        "status": "LOST",
        "reason": "Rejected for first-customer fit.",
        "city": None,
        "tags": ["first_customer_fit_rejected"],
    },
    {
        "key": "gd-asesoria-first-fit-rejection",
        "company": "GD Asesoría",
        "domain": "gdasesoria.com",
        "buyer": None,
        "status": "LOST",
        "reason": "Rejected for first-customer fit.",
        "city": None,
        "tags": ["first_customer_fit_rejected"],
    },
    {
        "key": "karma-buyer-unresolved",
        "company": "Karma Asesores",
        "domain": "k-asesores.com",
        "buyer": None,
        "buyer_role": "Managing Partner / Socio Director",
        "status": "TO_CONTACT",
        "reason": "Buyer hypothesis exists, but no LinkedIn profile was found.",
        "city": "Madrid",
        "tags": ["buyer_inaccessible", "no_linkedin_found"],
    },
    {
        "key": "carsan-buyer-unresolved",
        "company": "Carsán Gestión",
        "domain": "carsangestion.es",
        "buyer": None,
        "buyer_role": "Managing Director / Partner",
        "status": "TO_CONTACT",
        "reason": "Good prospect; the individual buyer is still unresolved.",
        "city": "Madrid",
        "tags": ["buyer_unresolved", "standard_software_integration_opportunity"],
    },
]


def seed_current_commercial_state(db: Session) -> dict[str, int]:
    opportunity = default_opportunity(db)
    created_companies = 0
    created_contacts = 0
    created_events = 0
    created_notes = 0

    for row in CURRENT_COMMERCIAL_STATE:
        company = db.scalar(select(Company).where(Company.domain == row["domain"]))
        if company is None:
            company = Company(
                name=row["company"],
                domain=row["domain"],
                website_url=f"https://{row['domain']}",
                industry="professional_services",
                country="Spain",
                city=row["city"],
            )
            db.add(company)
            db.flush()
            created_companies += 1

        buyer_name = row.get("buyer")
        buyer_role = row.get("buyer_role")
        contact = _primary_contact(db, company.id)
        if (buyer_name or buyer_role) and contact is None:
            contact = Contact(
                company_id=company.id,
                full_name=buyer_name,
                role=buyer_role,
                channel="LINKEDIN",
                is_primary=True,
                notes="Profile URL not recorded; validate manually before future outreach.",
            )
            db.add(contact)
            db.flush()
            created_contacts += 1

        if row["status"] == "TO_CONTACT":
            if not _note_exists(db, company.id, row["reason"]):
                db.add(
                    CommercialNote(
                        company_id=company.id,
                        contact_id=contact.id if contact else None,
                        opportunity_id=opportunity.id,
                        body=row["reason"],
                        learning_tags=row["tags"],
                        evidence_ids=[],
                    )
                )
                created_notes += 1
            continue

        if _seed_event_exists(db, company.id, row["key"]):
            continue
        state = current_pipeline_state(db, company.id, opportunity.id)
        if row["status"] == "CONNECTION_SENT" and state is None:
            transition_pipeline(
                db,
                company_id=company.id,
                opportunity_id=opportunity.id,
                to_state="APPROVED",
                notes="Historical manual outreach record imported.",
                metadata={"seed_parent": row["key"]},
            )
            event = transition_pipeline(
                db,
                company_id=company.id,
                opportunity_id=opportunity.id,
                to_state="CONNECTION_SENT",
                notes=(
                    "Connection request was sent manually. Exact send time and note text were "
                    "not supplied."
                ),
                metadata={
                    "seed_key": row["key"],
                    "action": "MARK_CONNECTION_SENT",
                    "connection_note_type": row["note_type"],
                    "message_version": "manual-unrecorded",
                    "message_text_missing": True,
                    "contacted_at_unknown": True,
                    "evidence_ids": [],
                    "outreach_reason": row["reason"],
                    "learning_tags": row["tags"],
                },
                channel="LINKEDIN",
                message_used=None,
            )
            event.contacted_at = None
            db.commit()
            created_events += 2
        elif row["status"] == "LOST" and state is None:
            transition_pipeline(
                db,
                company_id=company.id,
                opportunity_id=opportunity.id,
                to_state="LOST",
                notes=row["reason"],
                metadata={
                    "seed_key": row["key"],
                    "action": "MARK_REJECTED",
                    "learning_tags": row["tags"],
                },
                lost_reason=row["reason"],
            )
            created_events += 1

    db.commit()
    return {
        "companies": created_companies,
        "contacts": created_contacts,
        "events": created_events,
        "notes": created_notes,
    }


def _primary_contact(db: Session, company_id: int) -> Contact | None:
    return db.scalar(
        select(Contact)
        .where(Contact.company_id == company_id, Contact.is_primary.is_(True))
        .order_by(Contact.id.desc())
    )


def _seed_event_exists(db: Session, company_id: int, seed_key: str) -> bool:
    events = db.scalars(select(PipelineEvent).where(PipelineEvent.company_id == company_id))
    return any(event.event_metadata.get("seed_key") == seed_key for event in events)


def _note_exists(db: Session, company_id: int, body: str) -> bool:
    return (
        db.scalar(
            select(CommercialNote).where(
                CommercialNote.company_id == company_id,
                CommercialNote.body == body,
            )
        )
        is not None
    )


if __name__ == "__main__":
    with SessionLocal() as session:
        print(seed_current_commercial_state(session))
