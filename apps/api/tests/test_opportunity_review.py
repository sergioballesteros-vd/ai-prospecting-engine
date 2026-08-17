from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.application.opportunity_review import (
    generate_outreach_draft,
    score_company_for_opportunity,
    update_outreach_draft,
    update_score_state,
    upsert_opportunity_score,
)
from app.domain.models import Base, Company, Evidence, Opportunity
from app.modules.research.website import evidence_fingerprint


def test_scoring_is_deterministic_and_explainable() -> None:
    company = Company(
        id=1,
        name="Acme Clinics",
        domain="acme.example",
        website_url="https://acme.example",
        country="Spain",
        industry="private_clinics",
    )
    opportunity = _opportunity()
    evidence = [
        _evidence(1, "HAS_CRM", 0.8),
        _evidence(2, "MULTIPLE_CONTACT_FORMS", 0.7),
        _evidence(3, "HAS_SALES_TEAM", 0.6),
    ]

    first = score_company_for_opportunity(company, opportunity, evidence)
    second = score_company_for_opportunity(company, opportunity, evidence)

    assert first == second
    assert first.total_score > 60
    assert first.qualification_state == "QUALIFIED"
    assert "Acme Clinics matched Sales Operations Automation" in first.explanation


def test_score_persists_traceable_evidence_ids() -> None:
    db = _session()
    company, opportunity = _persist_company_opportunity_and_evidence(db)

    score = upsert_opportunity_score(db, company, opportunity)

    assert score.evidence_ids
    assert set(score.evidence_ids).issubset({item.id for item in company.evidence})
    assert "HAS_CRM" in score.matched_signals


def test_state_transitions_are_limited_to_review_states() -> None:
    db = _session()
    company, opportunity = _persist_company_opportunity_and_evidence(db)
    score = upsert_opportunity_score(db, company, opportunity)
    db.commit()

    approved = update_score_state(db, score.id, "APPROVED")

    assert approved.qualification_state == "APPROVED"


def test_draft_generation_requires_approval_and_persists_evidence_ids() -> None:
    db = _session()
    company, opportunity = _persist_company_opportunity_and_evidence(db)
    score = upsert_opportunity_score(db, company, opportunity)
    db.commit()

    update_score_state(db, score.id, "APPROVED")
    draft = generate_outreach_draft(db, score.id)

    assert draft.status == "DRAFT"
    assert draft.evidence_used == score.evidence_ids
    assert "I do not want to assume" in draft.body

    updated = update_outreach_draft(db, draft.id, "Edited subject", "Edited body")

    assert updated.subject == "Edited subject"
    assert updated.body == "Edited body"
    assert updated.evidence_used == draft.evidence_used


def _session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def _persist_company_opportunity_and_evidence(db: Session) -> tuple[Company, Opportunity]:
    company = Company(
        name="Acme Clinics",
        domain="acme.example",
        website_url="https://acme.example",
        country="Spain",
        industry="private_clinics",
    )
    opportunity = _opportunity()
    db.add_all([company, opportunity])
    db.flush()
    db.add_all(
        [
            _evidence(None, "HAS_CRM", 0.8, company.id),
            _evidence(None, "MULTIPLE_CONTACT_FORMS", 0.7, company.id),
            _evidence(None, "HAS_SALES_TEAM", 0.6, company.id),
        ]
    )
    db.commit()
    db.refresh(company)
    return company, opportunity


def _opportunity() -> Opportunity:
    return Opportunity(
        name="Sales Operations Automation",
        market={
            "country": "Spain",
            "company_size": {"min": 10, "max": 150},
            "industries": ["private_clinics", "education", "professional_services"],
        },
        desired_signals=["HAS_CRM", "MULTIPLE_CONTACT_FORMS", "HAS_SALES_TEAM"],
        excluded_industries=["energy"],
        weights={"icp": 0.30, "pain": 0.30, "value": 0.20, "intent": 0.10, "reachability": 0.10},
    )


def _evidence(
    evidence_id: int | None, signal_type: str, confidence: float, company_id: int = 1
) -> Evidence:
    evidence = Evidence(
        company_id=company_id,
        signal_type=signal_type,
        source_url="https://acme.example",
        content_excerpt=f"Public evidence for {signal_type}",
        fingerprint=evidence_fingerprint(
            signal_type, "https://acme.example", f"Public evidence for {signal_type}"
        ),
        confidence=confidence,
        evidence_metadata={"test": True},
    )
    if evidence_id is not None:
        evidence.id = evidence_id
    return evidence
