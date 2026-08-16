from collections import defaultdict
from datetime import UTC, datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.domain.models import (
    CampaignCompany,
    Company,
    OpportunityScore,
    PipelineEvent,
    ProspectingCampaign,
)

PIPELINE_STATES = ["APPROVED", "CONTACTED", "REPLIED", "MEETING", "PROPOSAL", "WON", "LOST"]
VALID_TRANSITIONS = {
    None: {"APPROVED"},
    "APPROVED": {"CONTACTED", "LOST"},
    "CONTACTED": {"REPLIED", "LOST"},
    "REPLIED": {"MEETING", "LOST"},
    "MEETING": {"PROPOSAL", "LOST"},
    "PROPOSAL": {"WON", "LOST"},
}
CHANNELS = {"EMAIL", "LINKEDIN", "PHONE", "OTHER"}


def transition_pipeline(
    db: Session,
    *,
    company_id: int,
    opportunity_id: int,
    to_state: str,
    campaign_id: int | None = None,
    notes: str | None = None,
    metadata: dict | None = None,
    channel: str | None = None,
    contacted_at: datetime | None = None,
    message_used: str | None = None,
    expected_revenue: float | None = None,
    recurring_revenue_monthly: float | None = None,
    implementation_revenue: float | None = None,
    currency: str | None = None,
    closed_at: datetime | None = None,
    lost_reason: str | None = None,
) -> PipelineEvent:
    if to_state not in PIPELINE_STATES:
        raise ValueError(f"Invalid pipeline state: {to_state}")
    company = db.get(Company, company_id)
    if company is None:
        raise ValueError("Company not found")
    from_state = current_pipeline_state(db, company_id, opportunity_id, campaign_id)
    if to_state not in VALID_TRANSITIONS.get(from_state, set()):
        raise ValueError(f"Invalid transition from {from_state or 'START'} to {to_state}")
    if to_state == "CONTACTED":
        if channel not in CHANNELS:
            raise ValueError("CONTACTED requires channel EMAIL, LINKEDIN, PHONE, or OTHER")
        contacted_at = contacted_at or datetime.now(UTC)
    if to_state == "WON":
        missing_revenue = (
            expected_revenue is None
            and recurring_revenue_monthly is None
            and implementation_revenue is None
        )
        if missing_revenue:
            raise ValueError("WON requires revenue information")
        currency = currency or "EUR"
        closed_at = closed_at or datetime.now(UTC)
    if to_state == "LOST" and not lost_reason:
        raise ValueError("LOST requires lost_reason")

    event = PipelineEvent(
        company_id=company_id,
        campaign_id=campaign_id,
        opportunity_id=opportunity_id,
        from_state=from_state,
        to_state=to_state,
        notes=notes,
        event_metadata=metadata or {},
        channel=channel,
        contacted_at=contacted_at,
        message_used=message_used,
        expected_revenue=expected_revenue,
        recurring_revenue_monthly=recurring_revenue_monthly,
        implementation_revenue=implementation_revenue,
        currency=currency,
        closed_at=closed_at,
        lost_reason=lost_reason,
    )
    db.add(event)
    if to_state == "APPROVED":
        score = _score_for(db, company_id, opportunity_id)
        if score is not None:
            score.qualification_state = "APPROVED"
    db.commit()
    db.refresh(event)
    return event


def current_pipeline_state(
    db: Session, company_id: int, opportunity_id: int, campaign_id: int | None = None
) -> str | None:
    query = (
        select(PipelineEvent)
        .where(
            PipelineEvent.company_id == company_id,
            PipelineEvent.opportunity_id == opportunity_id,
        )
        .order_by(PipelineEvent.timestamp.desc(), PipelineEvent.id.desc())
    )
    if campaign_id is None:
        query = query.where(PipelineEvent.campaign_id.is_(None))
    else:
        query = query.where(
            or_(
                PipelineEvent.campaign_id == campaign_id,
                PipelineEvent.campaign_id.is_(None),
            )
        )
    event = db.scalar(query)
    return event.to_state if event else None


def timeline_for_company(db: Session, company_id: int) -> list[PipelineEvent]:
    return list(
        db.scalars(
            select(PipelineEvent)
            .where(PipelineEvent.company_id == company_id)
            .order_by(PipelineEvent.timestamp.asc(), PipelineEvent.id.asc())
        )
    )


def funnel_metrics(db: Session, campaign_id: int | None = None) -> dict:
    campaigns = _campaigns_for_metrics(db, campaign_id)
    events = _pipeline_events(db, campaign_id)
    reached = _reached_states(events)
    discovered = sum(len(campaign.companies) for campaign in campaigns)
    researched = sum(
        1
        for campaign in campaigns
        for entry in campaign.companies
        if entry.research_state == "RESEARCHED"
    )
    qualified = _qualified_count(campaigns)
    approved = max(reached["APPROVED"], _approved_score_count(campaigns))
    contacted = reached["CONTACTED"]
    replied = reached["REPLIED"]
    meetings = reached["MEETING"]
    proposals = reached["PROPOSAL"]
    won = reached["WON"]
    lost = reached["LOST"]
    revenue = sum((event.expected_revenue or 0) for event in events if event.to_state == "WON")
    mrr = sum((event.recurring_revenue_monthly or 0) for event in events if event.to_state == "WON")
    research_cost = sum(
        run.estimated_cost for campaign in campaigns for run in campaign.research_runs
    )
    return {
        "counts": {
            "discovered": discovered,
            "researched": researched,
            "qualified": qualified,
            "approved": approved,
            "contacted": contacted,
            "replied": replied,
            "meetings": meetings,
            "proposals": proposals,
            "won": won,
            "lost": lost,
        },
        "conversion_rates": {
            "contacted_to_reply": _rate(replied, contacted),
            "reply_to_meeting": _rate(meetings, replied),
            "meeting_to_proposal": _rate(proposals, meetings),
            "proposal_to_won": _rate(won, proposals),
        },
        "business_metrics": {
            "revenue_generated": round(revenue, 2),
            "mrr_generated": round(mrr, 2),
            "average_deal_value": round(revenue / won, 2) if won else 0,
            "revenue_per_100_discovered": round(_per_100(revenue, discovered), 2),
            "revenue_per_100_contacted": round(_per_100(revenue, contacted), 2),
            "research_cost_per_meeting": round(research_cost / meetings, 6) if meetings else 0,
            "research_cost_per_won_customer": round(research_cost / won, 6) if won else 0,
            "research_cost": round(research_cost, 6),
        },
    }


def campaign_comparison(db: Session) -> list[dict]:
    rows = []
    for campaign in _campaigns_for_metrics(db, None):
        metrics = funnel_metrics(db, campaign.id)
        counts = metrics["counts"]
        business = metrics["business_metrics"]
        conversions = metrics["conversion_rates"]
        rows.append(
            {
                "campaign_id": campaign.id,
                "name": campaign.name,
                "sector": ", ".join(campaign.industries),
                "companies_discovered": counts["discovered"],
                "qualified": counts["qualified"],
                "reply_rate": conversions["contacted_to_reply"],
                "meeting_rate": conversions["reply_to_meeting"],
                "win_rate": conversions["proposal_to_won"],
                "revenue": business["revenue_generated"],
                "mrr": business["mrr_generated"],
                "research_cost": business["research_cost"],
            }
        )
    return rows


def _score_for(db: Session, company_id: int, opportunity_id: int) -> OpportunityScore | None:
    return db.scalar(
        select(OpportunityScore).where(
            OpportunityScore.company_id == company_id,
            OpportunityScore.opportunity_id == opportunity_id,
        )
    )


def _campaigns_for_metrics(db: Session, campaign_id: int | None) -> list[ProspectingCampaign]:
    query = select(ProspectingCampaign).options(
        selectinload(ProspectingCampaign.companies)
        .selectinload(CampaignCompany.company)
        .selectinload(Company.opportunity_scores),
        selectinload(ProspectingCampaign.research_runs),
    )
    if campaign_id is not None:
        query = query.where(ProspectingCampaign.id == campaign_id)
    return list(db.scalars(query).all())


def _pipeline_events(db: Session, campaign_id: int | None) -> list[PipelineEvent]:
    query = select(PipelineEvent)
    if campaign_id is not None:
        campaign = db.get(ProspectingCampaign, campaign_id)
        if campaign is None:
            return []
        campaign_company_ids = select(CampaignCompany.company_id).where(
            CampaignCompany.campaign_id == campaign_id
        )
        query = query.where(
            PipelineEvent.company_id.in_(campaign_company_ids),
            PipelineEvent.opportunity_id == campaign.opportunity_id,
            or_(
                PipelineEvent.campaign_id == campaign_id,
                PipelineEvent.campaign_id.is_(None),
            ),
        )
    return list(db.scalars(query).all())


def _reached_states(events: list[PipelineEvent]) -> dict[str, int]:
    reached: dict[str, set[tuple[int, int | None, int]]] = defaultdict(set)
    for event in events:
        key = (event.company_id, event.campaign_id, event.opportunity_id)
        reached[event.to_state].add(key)
    return {state: len(reached[state]) for state in PIPELINE_STATES}


def _qualified_count(campaigns: list[ProspectingCampaign]) -> int:
    return sum(
        1
        for campaign in campaigns
        for entry in campaign.companies
        for score in entry.company.opportunity_scores
        if score.opportunity_id == campaign.opportunity_id
        and score.qualification_state in {"QUALIFIED", "APPROVED"}
    )


def _approved_score_count(campaigns: list[ProspectingCampaign]) -> int:
    return sum(
        1
        for campaign in campaigns
        for entry in campaign.companies
        for score in entry.company.opportunity_scores
        if score.opportunity_id == campaign.opportunity_id
        and score.qualification_state == "APPROVED"
    )


def _rate(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0


def _per_100(value: float, count: int) -> float:
    return (value / count) * 100 if count else 0
