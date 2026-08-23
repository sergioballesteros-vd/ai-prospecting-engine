from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.domain.models import (
    Company,
    Evidence,
    FirstCustomerFitScore,
    Opportunity,
    OpportunityScore,
    OutreachDraft,
)

REVIEW_STATES = {"RESEARCHED", "QUALIFIED", "REJECTED", "APPROVED"}


@dataclass(frozen=True)
class ScoreResult:
    icp_score: float
    pain_score: float
    value_score: float
    intent_score: float
    reachability_score: float
    confidence_score: float
    total_score: float
    explanation: str
    evidence_ids: list[int]
    matched_signals: list[str]
    qualification_state: str


@dataclass(frozen=True)
class FirstCustomerFitResult:
    size_fit: float
    buyer_accessibility: float
    workflow_fit: float
    automation_gap: float
    sales_simplicity: float
    implementation_fit: float
    confidence: float
    total_score: float
    positive_reasons: list[str]
    negative_reasons: list[str]
    disqualifiers: list[str]
    evidence_ids: list[int]
    matched_signals: list[str]
    explanation: str


POSITIVE_FIRST_CUSTOMER_SIGNALS = {
    "OWNER_LED",
    "MANAGING_PARTNER_VISIBLE",
    "SMALL_LOCAL_TEAM",
    "STANDARD_VERTICAL_SOFTWARE",
    "MULTIPLE_ADVISORY_AREAS",
    "DOCUMENT_HEAVY_WORKFLOW",
    "CLIENT_INTAKE_FLOW",
    "MANUAL_HANDOFF_HYPOTHESIS",
    "DIRECT_CONTACT_PATH",
    "LOCAL_OFFICE",
    "NO_INTERNAL_TECH_TEAM_VISIBLE",
}

FIRST_CUSTOMER_DISQUALIFIER_SIGNALS = {
    "PROPRIETARY_ERP",
    "PROPRIETARY_PLATFORM",
    "SELLS_TECH_TO_OTHER_FIRMS",
    "INTERNAL_PRODUCT_TEAM",
    "INTERNAL_ENGINEERING_TEAM",
    "EXPLICIT_AI_AUTOMATION_PROGRAM",
    "ENTERPRISE_SCALE",
    "MULTINATIONAL_COMPLEXITY",
    "LONG_PROCUREMENT_RISK",
}


def score_company_for_opportunity(
    company: Company, opportunity: Opportunity, evidence: list[Evidence]
) -> ScoreResult:
    signal_to_evidence = _best_evidence_by_signal(evidence)
    signals = set(signal_to_evidence)
    icp = _icp_score(company, opportunity)
    pain = _weighted_signal_score(
        signals,
        {
            "HAS_CRM": 18,
            "USES_HUBSPOT": 22,
            "USES_SALESFORCE": 22,
            "USES_PIPEDRIVE": 20,
            "MULTIPLE_LOCATIONS": 18,
            "MULTIPLE_CONTACT_FORMS": 16,
            "HAS_SALES_TEAM": 16,
            "HAS_API": 10,
        },
        baseline=15 if evidence else 0,
    )
    value = _weighted_signal_score(
        signals,
        {
            "MULTIPLE_LOCATIONS": 24,
            "MULTIPLE_CONTACT_FORMS": 22,
            "HAS_CRM": 16,
            "HAS_API": 12,
            "HAS_SALES_TEAM": 12,
            "USES_HUBSPOT": 10,
            "USES_SALESFORCE": 10,
            "USES_PIPEDRIVE": 10,
        },
        baseline=20 if evidence else 0,
    )
    intent = _weighted_signal_score(
        signals,
        {
            "HIRING_SALES": 35,
            "ACTIVE_GROWTH_SIGNAL": 30,
            "HIRING_OPERATIONS": 25,
            "PUBLIC_WEBSITE_AVAILABLE": 8,
        },
        baseline=10 if evidence else 0,
    )
    reachability = _weighted_signal_score(
        signals,
        {
            "MULTIPLE_CONTACT_FORMS": 30,
            "HAS_SALES_TEAM": 24,
            "USES_CALENDLY": 18,
            "PUBLIC_WEBSITE_AVAILABLE": 16,
        },
        baseline=20 if evidence else 0,
    )
    confidence = _confidence_score(evidence)
    weights = _normalized_weights(opportunity.weights)
    total = round(
        icp * weights["icp"]
        + pain * weights["pain"]
        + value * weights["value"]
        + intent * weights["intent"]
        + reachability * weights["reachability"],
        2,
    )
    signals_by_confidence = sorted(
        signals, key=lambda name: signal_to_evidence[name].confidence, reverse=True
    )
    evidence_ids = [signal_to_evidence[signal].id for signal in signals_by_confidence][:5]
    matched_signals = sorted(signals)
    state = "QUALIFIED" if total >= 60 and confidence >= 35 else "RESEARCHED"
    return ScoreResult(
        icp_score=round(icp, 2),
        pain_score=round(pain, 2),
        value_score=round(value, 2),
        intent_score=round(intent, 2),
        reachability_score=round(reachability, 2),
        confidence_score=round(confidence, 2),
        total_score=total,
        explanation=_explain_score(company, opportunity, matched_signals, evidence_ids),
        evidence_ids=evidence_ids,
        matched_signals=matched_signals,
        qualification_state=state,
    )


def score_company_for_first_customer_fit(
    company: Company, evidence: list[Evidence]
) -> FirstCustomerFitResult:
    signal_to_evidence = _best_evidence_by_signal(evidence)
    signals = set(signal_to_evidence)
    positive_reasons: list[str] = []
    negative_reasons: list[str] = []
    disqualifiers = sorted(signals & FIRST_CUSTOMER_DISQUALIFIER_SIGNALS)

    size_fit = _first_customer_size_fit(company, signals, positive_reasons, negative_reasons)
    buyer_accessibility = _first_customer_buyer_accessibility(
        company, signals, positive_reasons, negative_reasons
    )
    workflow_fit = _first_customer_workflow_fit(signals, positive_reasons)
    automation_gap = _first_customer_automation_gap(signals, positive_reasons, negative_reasons)
    sales_simplicity = _first_customer_sales_simplicity(
        company, signals, positive_reasons, negative_reasons
    )
    implementation_fit = _first_customer_implementation_fit(
        signals, positive_reasons, negative_reasons
    )
    confidence = _confidence_score(evidence)
    penalty = min(len(disqualifiers) * 12, 42)
    total = round(
        _clamp(
            size_fit * 0.18
            + buyer_accessibility * 0.18
            + workflow_fit * 0.20
            + automation_gap * 0.18
            + sales_simplicity * 0.14
            + implementation_fit * 0.12
            - penalty
        ),
        2,
    )
    matched_signals = sorted(signals)
    evidence_ids = _first_customer_evidence_ids(signal_to_evidence, matched_signals)

    return FirstCustomerFitResult(
        size_fit=round(size_fit, 2),
        buyer_accessibility=round(buyer_accessibility, 2),
        workflow_fit=round(workflow_fit, 2),
        automation_gap=round(automation_gap, 2),
        sales_simplicity=round(sales_simplicity, 2),
        implementation_fit=round(implementation_fit, 2),
        confidence=round(confidence, 2),
        total_score=total,
        positive_reasons=positive_reasons,
        negative_reasons=negative_reasons,
        disqualifiers=disqualifiers,
        evidence_ids=evidence_ids,
        matched_signals=matched_signals,
        explanation=_explain_first_customer_fit(company, positive_reasons, negative_reasons),
    )


def upsert_first_customer_fit_score(db: Session, company: Company) -> FirstCustomerFitScore:
    evidence = list(company.evidence)
    result = score_company_for_first_customer_fit(company, evidence)
    score = db.scalar(
        select(FirstCustomerFitScore).where(FirstCustomerFitScore.company_id == company.id)
    )
    if score is None:
        score = FirstCustomerFitScore(company_id=company.id)
        db.add(score)
    score.size_fit = result.size_fit
    score.buyer_accessibility = result.buyer_accessibility
    score.workflow_fit = result.workflow_fit
    score.automation_gap = result.automation_gap
    score.sales_simplicity = result.sales_simplicity
    score.implementation_fit = result.implementation_fit
    score.confidence = result.confidence
    score.total_score = result.total_score
    score.positive_reasons = result.positive_reasons
    score.negative_reasons = result.negative_reasons
    score.disqualifiers = result.disqualifiers
    score.evidence_ids = result.evidence_ids
    score.matched_signals = result.matched_signals
    score.explanation = result.explanation
    score.updated_at = datetime.now(UTC)
    db.flush()
    return score


def upsert_opportunity_score(
    db: Session, company: Company, opportunity: Opportunity
) -> OpportunityScore:
    evidence = list(company.evidence)
    result = score_company_for_opportunity(company, opportunity, evidence)
    score = db.scalar(
        select(OpportunityScore).where(
            OpportunityScore.company_id == company.id,
            OpportunityScore.opportunity_id == opportunity.id,
        )
    )
    if score is None:
        score = OpportunityScore(company_id=company.id, opportunity_id=opportunity.id)
        db.add(score)
    score.icp_score = result.icp_score
    score.pain_score = result.pain_score
    score.value_score = result.value_score
    score.intent_score = result.intent_score
    score.reachability_score = result.reachability_score
    score.confidence_score = result.confidence_score
    score.total_score = result.total_score
    if score.qualification_state not in {"APPROVED", "REJECTED"}:
        score.qualification_state = result.qualification_state
    score.explanation = result.explanation
    score.evidence_ids = result.evidence_ids
    score.matched_signals = result.matched_signals
    score.updated_at = datetime.now(UTC)
    db.flush()
    return score


def score_all_researched_companies(db: Session) -> list[OpportunityScore]:
    opportunity = default_opportunity(db)
    companies = db.scalars(
        select(Company)
        .options(selectinload(Company.evidence))
        .where(Company.evidence.any())
        .order_by(Company.created_at.desc())
    ).all()
    scores = []
    for company in companies:
        scores.append(upsert_opportunity_score(db, company, opportunity))
        upsert_first_customer_fit_score(db, company)
    db.commit()
    return scores


def ranked_opportunity_scores(db: Session) -> list[OpportunityScore]:
    score_all_researched_companies(db)
    scores = list(
        db.scalars(
            select(OpportunityScore)
            .options(
                selectinload(OpportunityScore.company).selectinload(Company.evidence),
                selectinload(OpportunityScore.company).selectinload(
                    Company.first_customer_fit_scores
                ),
                selectinload(OpportunityScore.outreach_drafts),
            )
            .order_by(OpportunityScore.updated_at.desc())
        ).all()
    )
    return sorted(
        scores,
        key=lambda score: (
            score.company.first_customer_fit_scores[0].total_score
            if score.company.first_customer_fit_scores
            else -1,
            score.total_score,
            score.updated_at,
        ),
        reverse=True,
    )


def update_score_state(db: Session, score_id: int, state: str) -> OpportunityScore:
    if state not in REVIEW_STATES:
        raise ValueError(f"Invalid qualification state: {state}")
    score = db.get(OpportunityScore, score_id)
    if score is None:
        raise ValueError("Opportunity score not found")
    score.qualification_state = state
    score.updated_at = datetime.now(UTC)
    db.commit()
    db.refresh(score)
    return score


def generate_outreach_draft(db: Session, score_id: int) -> OutreachDraft:
    score = db.scalar(
        select(OpportunityScore)
        .where(OpportunityScore.id == score_id)
        .options(selectinload(OpportunityScore.company).selectinload(Company.evidence))
    )
    if score is None:
        raise ValueError("Opportunity score not found")
    if score.qualification_state != "APPROVED":
        raise ValueError("Drafts can only be generated for APPROVED companies")

    evidence = _evidence_by_ids(score.company.evidence, score.evidence_ids)
    if not evidence:
        raise ValueError("Cannot generate a draft without traceable evidence")

    subject = f"Possible automation opportunity at {score.company.name}"
    body = _draft_body(score.company, evidence)
    draft = OutreachDraft(
        company_id=score.company_id,
        opportunity_id=score.opportunity_id,
        opportunity_score_id=score.id,
        channel="email",
        subject=subject,
        body=body,
        evidence_used=[item.id for item in evidence],
        status="DRAFT",
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft


def update_outreach_draft(
    db: Session, draft_id: int, subject: str, body: str, status: str | None = None
) -> OutreachDraft:
    draft = db.get(OutreachDraft, draft_id)
    if draft is None:
        raise ValueError("Outreach draft not found")
    draft.subject = subject
    draft.body = body
    if status is not None:
        if status not in {"DRAFT", "READY_FOR_REVIEW"}:
            raise ValueError("Invalid draft status")
        draft.status = status
    draft.updated_at = datetime.now(UTC)
    db.commit()
    db.refresh(draft)
    return draft


def default_opportunity(db: Session) -> Opportunity:
    opportunity = db.scalar(select(Opportunity).order_by(Opportunity.id.asc()))
    if opportunity is None:
        raise ValueError("Default opportunity is not seeded")
    return opportunity


def _best_evidence_by_signal(evidence: list[Evidence]) -> dict[str, Evidence]:
    signal_to_evidence: dict[str, Evidence] = {}
    for item in sorted(evidence, key=lambda row: row.confidence, reverse=True):
        signal_to_evidence.setdefault(item.signal_type, item)
    return signal_to_evidence


def _first_customer_size_fit(
    company: Company,
    signals: set[str],
    positive_reasons: list[str],
    negative_reasons: list[str],
) -> float:
    if "ENTERPRISE_SCALE" in signals:
        negative_reasons.append("Enterprise-scale signal makes this a poor first-customer fit.")
        return 20
    if company.employee_estimate is None:
        positive_reasons.append("Employee count is unknown; size fit is scored conservatively.")
        return 55
    if 5 <= company.employee_estimate <= 50:
        positive_reasons.append("Estimated 5-50 employee range fits the first-customer ICP.")
        return 92
    if 51 <= company.employee_estimate <= 100:
        negative_reasons.append("Estimated 51-100 employees may add some sales complexity.")
        return 62
    negative_reasons.append("Estimated 100+ employees creates first-customer sales complexity.")
    return 28


def _first_customer_buyer_accessibility(
    company: Company,
    signals: set[str],
    positive_reasons: list[str],
    negative_reasons: list[str],
) -> float:
    score = 45.0
    if signals & {"OWNER_LED", "MANAGING_PARTNER_VISIBLE"}:
        score += 30
        positive_reasons.append("Owner, partner, or managing partner visibility supports access.")
    if signals & {"DIRECT_CONTACT_PATH", "LOCAL_OFFICE", "SMALL_LOCAL_TEAM"}:
        score += 20
        positive_reasons.append("Local/direct contact path supports buyer access.")
    if company.city and company.city.lower() in {"madrid", "comunidad de madrid"}:
        score += 8
        positive_reasons.append("Madrid-region presence fits the initial commercial focus.")
    if signals & {"MULTINATIONAL_COMPLEXITY", "LONG_PROCUREMENT_RISK"}:
        score -= 35
        negative_reasons.append("Corporate hierarchy or procurement signals reduce buyer access.")
    return _clamp(score)


def _first_customer_workflow_fit(signals: set[str], positive_reasons: list[str]) -> float:
    score = 35.0
    workflow_signals = {
        "MULTIPLE_ADVISORY_AREAS",
        "DOCUMENT_HEAVY_WORKFLOW",
        "CLIENT_INTAKE_FLOW",
        "HAS_CONTACT_FORM",
        "HAS_SUPPORT_FLOW",
        "MULTIPLE_PRODUCTS_OR_SERVICES",
    }
    matched = signals & workflow_signals
    if matched:
        score += min(len(matched) * 16, 50)
        positive_reasons.append("Public evidence suggests recurring client/document workflows.")
    if "MANUAL_HANDOFF_HYPOTHESIS" in signals:
        score += 15
        positive_reasons.append("Evidence supports a manual handoff or routing hypothesis.")
    return _clamp(score)


def _first_customer_automation_gap(
    signals: set[str],
    positive_reasons: list[str],
    negative_reasons: list[str],
) -> float:
    score = 50.0
    if "STANDARD_VERTICAL_SOFTWARE" in signals:
        score += 18
        positive_reasons.append(
            "Standard vertical software can indicate integration gaps, not disqualification."
        )
    if signals & {"HAS_CRM_INDICATORS", "HAS_INTEGRATIONS", "USES_HUBSPOT"}:
        score += 10
        positive_reasons.append("Standard digital tooling may create before/after workflow gaps.")
    maturity_signals = signals & {
        "PROPRIETARY_ERP",
        "PROPRIETARY_PLATFORM",
        "SELLS_TECH_TO_OTHER_FIRMS",
        "INTERNAL_PRODUCT_TEAM",
        "INTERNAL_ENGINEERING_TEAM",
        "EXPLICIT_AI_AUTOMATION_PROGRAM",
    }
    if maturity_signals:
        score -= min(len(maturity_signals) * 22, 62)
        negative_reasons.append(
            "Internal technology maturity suggests the first implementation problem may be solved."
        )
    if "NO_INTERNAL_TECH_TEAM_VISIBLE" in signals:
        score += 10
        positive_reasons.append(
            "No visible internal tech team supports an external implementation fit."
        )
    return _clamp(score)


def _first_customer_sales_simplicity(
    company: Company,
    signals: set[str],
    positive_reasons: list[str],
    negative_reasons: list[str],
) -> float:
    score = 55.0
    if signals & {"SMALL_LOCAL_TEAM", "LOCAL_OFFICE", "OWNER_LED"}:
        score += 24
        positive_reasons.append("Local owner-led structure keeps sales motion simple.")
    if "MULTIPLE_LOCATIONS" in signals:
        score -= 10
        negative_reasons.append("Multiple locations can add coordination complexity.")
    if signals & {"MULTINATIONAL_COMPLEXITY", "LONG_PROCUREMENT_RISK", "ENTERPRISE_SCALE"}:
        score -= 32
        negative_reasons.append("Scale/procurement signals make the first sale harder.")
    if company.employee_estimate and company.employee_estimate > 100:
        score -= 20
    return _clamp(score)


def _first_customer_implementation_fit(
    signals: set[str],
    positive_reasons: list[str],
    negative_reasons: list[str],
) -> float:
    score = 58.0
    if signals & {"CLIENT_INTAKE_FLOW", "DOCUMENT_HEAVY_WORKFLOW", "STANDARD_VERTICAL_SOFTWARE"}:
        score += 24
        positive_reasons.append("A narrow intake/document workflow appears isolatable.")
    if signals & {"PROPRIETARY_ERP", "PROPRIETARY_PLATFORM"}:
        score -= 30
        negative_reasons.append("Proprietary core systems raise implementation expectations.")
    if "MULTINATIONAL_COMPLEXITY" in signals:
        score -= 18
    return _clamp(score)


def _first_customer_evidence_ids(
    signal_to_evidence: dict[str, Evidence], matched_signals: list[str]
) -> list[int]:
    prioritized = sorted(
        matched_signals,
        key=lambda signal: (
            signal in FIRST_CUSTOMER_DISQUALIFIER_SIGNALS,
            signal in POSITIVE_FIRST_CUSTOMER_SIGNALS,
            signal_to_evidence[signal].confidence,
        ),
        reverse=True,
    )
    ids = [
        signal_to_evidence[signal].id
        for signal in prioritized
        if signal_to_evidence[signal].id
    ]
    return ids[:8]


def _explain_first_customer_fit(
    company: Company, positive_reasons: list[str], negative_reasons: list[str]
) -> str:
    if not positive_reasons and not negative_reasons:
        return f"{company.name} has limited public evidence for first-customer fit."
    positives = " ".join(positive_reasons[:2])
    negatives = " ".join(negative_reasons[:2])
    if positives and negatives:
        return f"{positives} Main risks: {negatives}"
    return positives or f"Main risks: {negatives}"


def _icp_score(company: Company, opportunity: Opportunity) -> float:
    score = 35.0
    market = opportunity.market or {}
    if company.country and market.get("country"):
        score += 25 if company.country.lower() == str(market["country"]).lower() else -10
    elif not company.country:
        score += 10
    industries = {str(item).lower() for item in market.get("industries", [])}
    if company.industry and industries:
        score += 25 if company.industry.lower() in industries else 5
    elif not company.industry:
        score += 10
    size = market.get("company_size", {})
    if company.employee_estimate and size:
        if size.get("min", 0) <= company.employee_estimate <= size.get("max", 10**9):
            score += 25
        else:
            score += 5
    elif not company.employee_estimate:
        score += 15
    if company.industry and company.industry.lower() in {
        str(item).lower() for item in opportunity.excluded_industries
    }:
        score = min(score, 20)
    return _clamp(score)


def _weighted_signal_score(
    signals: set[str], weights: dict[str, float], baseline: float = 0
) -> float:
    return _clamp(baseline + sum(weight for signal, weight in weights.items() if signal in signals))


def _confidence_score(evidence: list[Evidence]) -> float:
    if not evidence:
        return 0
    average = sum(item.confidence for item in evidence) / len(evidence)
    count_bonus = min(len(evidence) * 5, 25)
    return _clamp(average * 75 + count_bonus)


def _normalized_weights(raw_weights: dict) -> dict[str, float]:
    defaults = {
        "icp": 0.30,
        "pain": 0.30,
        "value": 0.20,
        "intent": 0.10,
        "reachability": 0.10,
    }
    weights = {key: float(raw_weights.get(key, value)) for key, value in defaults.items()}
    total = sum(weights.values())
    return {key: value / total for key, value in weights.items()}


def _explain_score(
    company: Company, opportunity: Opportunity, matched_signals: list[str], evidence_ids: list[int]
) -> str:
    if matched_signals:
        signal_text = ", ".join(matched_signals[:5])
        evidence_text = ", ".join(f"#{item}" for item in evidence_ids[:5])
        return (
            f"{company.name} matched {opportunity.name} through observable signals "
            f"{signal_text}. Score is based on evidence {evidence_text}."
        )
    return f"{company.name} has limited public evidence for {opportunity.name}."


def _evidence_by_ids(evidence: list[Evidence], evidence_ids: list[int]) -> list[Evidence]:
    by_id = {item.id: item for item in evidence}
    return [by_id[item_id] for item_id in evidence_ids if item_id in by_id]


def _draft_body(company: Company, evidence: list[Evidence]) -> str:
    observations = "\n".join(
        f"- {item.signal_type}: {item.content_excerpt[:220]}" for item in evidence[:3]
    )
    return (
        f"Hi,\n\n"
        f"I was reviewing public information about {company.name} and noticed a few observable "
        f"signals that may be relevant to operations or sales-process automation:\n\n"
        f"{observations}\n\n"
        "I do not want to assume how your internal process works, but these signals suggest there "
        "may be a useful conversation around lead routing, follow-up, integrations, "
        "or reporting.\n\n"
        "Would it be worth a short conversation to understand whether any of this is relevant?"
    )


def _clamp(value: float) -> float:
    return max(0, min(100, value))
