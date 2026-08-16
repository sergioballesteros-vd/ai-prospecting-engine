import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.application.pipeline import (
    campaign_comparison,
    current_pipeline_state,
    funnel_metrics,
    transition_pipeline,
)
from app.domain.models import (
    Base,
    CampaignCompany,
    Company,
    Opportunity,
    OpportunityScore,
    ProspectingCampaign,
    ResearchRun,
)


def test_valid_transitions_preserve_event_history() -> None:
    db = _session()
    company, opportunity, campaign = _seed_pipeline_context(db)

    approved = transition_pipeline(
        db,
        company_id=company.id,
        opportunity_id=opportunity.id,
        campaign_id=campaign.id,
        to_state="APPROVED",
    )
    contacted = transition_pipeline(
        db,
        company_id=company.id,
        opportunity_id=opportunity.id,
        campaign_id=campaign.id,
        to_state="CONTACTED",
        channel="EMAIL",
        message_used="Manual message",
    )

    assert approved.from_state is None
    assert contacted.from_state == "APPROVED"
    assert [event.to_state for event in company.pipeline_events] == ["APPROVED", "CONTACTED"]


def test_invalid_state_transition_is_rejected() -> None:
    db = _session()
    company, opportunity, campaign = _seed_pipeline_context(db)

    with pytest.raises(ValueError):
        transition_pipeline(
            db,
            company_id=company.id,
            opportunity_id=opportunity.id,
            campaign_id=campaign.id,
            to_state="MEETING",
        )


def test_revenue_calculations_and_funnel_metrics() -> None:
    db = _session()
    company, opportunity, campaign = _seed_pipeline_context(db)
    for state, kwargs in [
        ("APPROVED", {}),
        ("CONTACTED", {"channel": "EMAIL"}),
        ("REPLIED", {}),
        ("MEETING", {}),
        ("PROPOSAL", {}),
        (
            "WON",
            {
                "expected_revenue": 12000,
                "recurring_revenue_monthly": 500,
                "implementation_revenue": 6000,
                "currency": "EUR",
            },
        ),
    ]:
        transition_pipeline(
            db,
            company_id=company.id,
            opportunity_id=opportunity.id,
            campaign_id=campaign.id,
            to_state=state,
            **kwargs,
        )

    metrics = funnel_metrics(db, campaign.id)

    assert metrics["counts"]["won"] == 1
    assert metrics["conversion_rates"]["proposal_to_won"] == 1
    assert metrics["business_metrics"]["revenue_generated"] == 12000
    assert metrics["business_metrics"]["mrr_generated"] == 500
    assert metrics["business_metrics"]["average_deal_value"] == 12000
    assert metrics["business_metrics"]["revenue_per_100_discovered"] == 1_200_000
    assert metrics["business_metrics"]["research_cost_per_won_customer"] == 12.5


def test_campaign_comparison() -> None:
    db = _session()
    company, opportunity, campaign = _seed_pipeline_context(db)
    transition_pipeline(
        db,
        company_id=company.id,
        opportunity_id=opportunity.id,
        campaign_id=campaign.id,
        to_state="APPROVED",
    )
    transition_pipeline(
        db,
        company_id=company.id,
        opportunity_id=opportunity.id,
        campaign_id=campaign.id,
        to_state="CONTACTED",
        channel="LINKEDIN",
    )
    transition_pipeline(
        db,
        company_id=company.id,
        opportunity_id=opportunity.id,
        campaign_id=campaign.id,
        to_state="LOST",
        lost_reason="No budget",
    )

    comparison = campaign_comparison(db)

    assert comparison[0]["sector"] == "training companies"
    assert comparison[0]["companies_discovered"] == 1
    assert comparison[0]["qualified"] == 1
    assert comparison[0]["research_cost"] == 12.5


def test_campaign_metrics_include_global_pipeline_events_for_member_company() -> None:
    db = _session()
    company, opportunity, campaign = _seed_pipeline_context(db)
    transition_pipeline(
        db,
        company_id=company.id,
        opportunity_id=opportunity.id,
        to_state="APPROVED",
    )
    transition_pipeline(
        db,
        company_id=company.id,
        opportunity_id=opportunity.id,
        to_state="CONTACTED",
        channel="EMAIL",
    )

    metrics = funnel_metrics(db, campaign.id)

    assert current_pipeline_state(db, company.id, opportunity.id, campaign.id) == "CONTACTED"
    assert metrics["counts"]["contacted"] == 1


def _session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)()


def _seed_pipeline_context(db: Session) -> tuple[Company, Opportunity, ProspectingCampaign]:
    opportunity = Opportunity(
        name="Sales Operations Automation",
        market={"country": "Spain", "industries": ["training companies"]},
        desired_signals=["HAS_CRM"],
        excluded_industries=["energy"],
        weights={"icp": 0.30, "pain": 0.30, "value": 0.20, "intent": 0.10, "reachability": 0.10},
    )
    company = Company(
        name="Training One",
        domain="training-one.example",
        website_url="https://training-one.example",
        industry="training companies",
        country="Spain",
        city="Madrid",
    )
    db.add_all([opportunity, company])
    db.flush()
    campaign = ProspectingCampaign(
        name="Training companies in Madrid",
        country="Spain",
        city_or_region="Madrid",
        industries=["training companies"],
        employee_min=10,
        employee_max=150,
        opportunity_id=opportunity.id,
        target_company_count=10,
        status="COMPLETED",
    )
    db.add(campaign)
    db.flush()
    db.add(
        CampaignCompany(
            campaign_id=campaign.id,
            company_id=company.id,
            discovery_source="test",
            discovery_metadata={},
            research_state="RESEARCHED",
        )
    )
    db.add(
        OpportunityScore(
            company_id=company.id,
            opportunity_id=opportunity.id,
            icp_score=80,
            pain_score=70,
            value_score=70,
            intent_score=50,
            reachability_score=60,
            confidence_score=80,
            total_score=70,
            qualification_state="QUALIFIED",
            explanation="Matched",
            evidence_ids=[],
            matched_signals=[],
        )
    )
    db.add(
        ResearchRun(
            company_id=company.id,
            campaign_id=campaign.id,
            provider="stub",
            model="deterministic-local",
            input_tokens=100,
            output_tokens=50,
            estimated_cost=12.5,
            execution_time_ms=1000,
            status="COMPLETED",
        )
    )
    db.commit()
    return company, opportunity, campaign
