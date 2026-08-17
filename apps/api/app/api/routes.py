from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.application.campaigns import (
    campaign_detail,
    campaign_stats,
    create_campaign,
    retry_campaign_company,
    run_campaign,
)
from app.application.opportunity_review import (
    generate_outreach_draft,
    ranked_opportunity_scores,
    update_outreach_draft,
    update_score_state,
)
from app.application.pipeline import (
    campaign_comparison,
    current_pipeline_state,
    funnel_metrics,
    timeline_for_company,
    transition_pipeline,
)
from app.application.research_jobs import create_research_job, get_research_job, run_research_job
from app.domain.models import Company, Evidence, OpportunityScore, ProspectingCampaign
from app.domain.schemas import (
    CampaignCompanyRead,
    CampaignCompanyResult,
    CampaignComparisonRead,
    CompanyCreate,
    CompanyDetail,
    CompanyRead,
    CompanyTimelineRead,
    FunnelAnalyticsRead,
    OutreachDraftRead,
    OutreachDraftUpdate,
    PipelineEventRead,
    PipelineTransitionCreate,
    ProspectingCampaignCreate,
    ProspectingCampaignDetail,
    ProspectingCampaignRead,
    RankedOpportunityRead,
    ResearchJobRead,
    ReviewStateUpdate,
)
from app.infrastructure.database import get_db
from app.modules.research.website import normalize_domain, website_url_for_domain

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/companies", response_model=CompanyRead)
def create_company(payload: CompanyCreate, db: DbSession) -> Company:
    try:
        domain = normalize_domain(payload.domain)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    existing = db.scalar(select(Company).where(Company.domain == domain))
    if existing:
        return existing

    company = Company(
        name=payload.name or domain.split(".")[0].replace("-", " ").title(),
        domain=domain,
        website_url=website_url_for_domain(domain),
        country=payload.country,
        city=payload.city,
        industry=payload.industry,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.get("/companies", response_model=list[CompanyRead])
def list_companies(db: DbSession) -> list[Company]:
    return list(db.scalars(select(Company).order_by(Company.created_at.desc())).all())


@router.get("/companies/{company_id}", response_model=CompanyDetail)
def get_company(company_id: int, db: DbSession) -> Company:
    company = db.scalar(
        select(Company)
        .where(Company.id == company_id)
        .options(
            selectinload(Company.sources),
            selectinload(Company.evidence),
            selectinload(Company.signals),
            selectinload(Company.analyses),
            selectinload(Company.research_runs),
        )
    )
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get("/companies/{company_id}/timeline", response_model=CompanyTimelineRead)
def get_company_timeline(company_id: int, db: DbSession):
    company = db.scalar(
        select(Company)
        .where(Company.id == company_id)
        .options(
            selectinload(Company.sources),
            selectinload(Company.evidence),
            selectinload(Company.signals),
            selectinload(Company.analyses),
            selectinload(Company.research_runs),
        )
    )
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return CompanyTimelineRead(
        id=company.id,
        name=company.name,
        domain=company.domain,
        website_url=company.website_url,
        industry=company.industry,
        country=company.country,
        city=company.city,
        created_at=company.created_at,
        sources=company.sources,
        evidence=company.evidence,
        signals=company.signals,
        analyses=company.analyses,
        research_runs=company.research_runs,
        timeline=timeline_for_company(db, company.id),
    )


@router.post("/companies/{company_id}/research", response_model=ResearchJobRead)
def start_research(company_id: int, background_tasks: BackgroundTasks, db: DbSession):
    if db.get(Company, company_id) is None:
        raise HTTPException(status_code=404, detail="Company not found")
    job = create_research_job(company_id, db)
    background_tasks.add_task(run_research_job, job.id)
    return job


@router.get("/research-jobs/{job_id}", response_model=ResearchJobRead)
def read_research_job(job_id: str):
    job = get_research_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Research job not found")
    return job


@router.get("/opportunities/ranked", response_model=list[RankedOpportunityRead])
def list_ranked_opportunities(db: DbSession) -> list[RankedOpportunityRead]:
    rows: list[RankedOpportunityRead] = []
    for score in ranked_opportunity_scores(db):
        evidence_by_id = {item.id: item for item in score.company.evidence}
        top_evidence = [
            evidence_by_id[item_id] for item_id in score.evidence_ids if item_id in evidence_by_id
        ]
        latest_draft = sorted(score.outreach_drafts, key=lambda item: item.id, reverse=True)
        rows.append(
            RankedOpportunityRead(
                score=score,
                company=score.company,
                top_evidence=top_evidence,
                why_matched=score.explanation,
                pipeline_state=current_pipeline_state(
                    db, score.company_id, score.opportunity_id
                ),
                latest_draft=latest_draft[0] if latest_draft else None,
            )
        )
    return rows


@router.patch("/opportunity-scores/{score_id}/state", response_model=RankedOpportunityRead)
def set_opportunity_score_state(
    score_id: int, payload: ReviewStateUpdate, db: DbSession
) -> RankedOpportunityRead:
    try:
        score = update_score_state(db, score_id, payload.state)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if payload.state == "APPROVED":
        try:
            if (
                current_pipeline_state(
                    db, score.company_id, score.opportunity_id, payload.campaign_id
                )
                is None
            ):
                transition_pipeline(
                    db,
                    company_id=score.company_id,
                    opportunity_id=score.opportunity_id,
                    campaign_id=payload.campaign_id,
                    to_state="APPROVED",
                    notes=payload.notes,
                )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    score = db.scalar(
        select(OpportunityScore)
        .where(OpportunityScore.id == score_id)
        .options(
            selectinload(OpportunityScore.company).selectinload(Company.evidence),
            selectinload(OpportunityScore.outreach_drafts),
        )
    )
    if score is None:
        raise HTTPException(status_code=404, detail="Opportunity score not found")
    evidence_by_id: dict[int, Evidence] = {item.id: item for item in score.company.evidence}
    return RankedOpportunityRead(
        score=score,
        company=score.company,
        top_evidence=[
            evidence_by_id[item_id] for item_id in score.evidence_ids if item_id in evidence_by_id
        ],
        why_matched=score.explanation,
        pipeline_state=current_pipeline_state(db, score.company_id, score.opportunity_id),
        latest_draft=sorted(score.outreach_drafts, key=lambda item: item.id, reverse=True)[0]
        if score.outreach_drafts
        else None,
    )


@router.post("/opportunity-scores/{score_id}/draft", response_model=OutreachDraftRead)
def create_score_draft(score_id: int, db: DbSession):
    try:
        return generate_outreach_draft(db, score_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch("/outreach-drafts/{draft_id}", response_model=OutreachDraftRead)
def edit_score_draft(draft_id: int, payload: OutreachDraftUpdate, db: DbSession):
    try:
        return update_outreach_draft(db, draft_id, payload.subject, payload.body, payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/campaigns", response_model=ProspectingCampaignRead)
def create_prospecting_campaign(payload: ProspectingCampaignCreate, db: DbSession):
    try:
        return create_campaign(
            db,
            name=payload.name,
            country=payload.country,
            city_or_region=payload.city_or_region,
            industries=payload.industries,
            employee_min=payload.employee_min,
            employee_max=payload.employee_max,
            opportunity_id=payload.opportunity_id,
            target_company_count=payload.target_company_count,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/campaigns", response_model=list[ProspectingCampaignRead])
def list_campaigns(db: DbSession):
    return list(
        db.scalars(select(ProspectingCampaign).order_by(ProspectingCampaign.created_at.desc()))
    )


@router.get("/campaigns/{campaign_id}", response_model=ProspectingCampaignDetail)
def read_campaign(campaign_id: int, db: DbSession):
    try:
        campaign = campaign_detail(db, campaign_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _campaign_detail_response(db, campaign)


@router.post("/campaigns/{campaign_id}/run", response_model=ProspectingCampaignRead)
def start_campaign(campaign_id: int, background_tasks: BackgroundTasks, db: DbSession):
    campaign = db.get(ProspectingCampaign, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.status == "RUNNING":
        return campaign
    background_tasks.add_task(run_campaign, campaign.id)
    campaign.status = "RUNNING"
    campaign.started_at = None
    db.commit()
    db.refresh(campaign)
    return campaign


@router.post("/campaign-companies/{entry_id}/retry", response_model=CampaignCompanyRead)
async def retry_campaign_entry(entry_id: int, db: DbSession):
    try:
        return await retry_campaign_company(db, entry_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/pipeline/events", response_model=PipelineEventRead)
def create_pipeline_event(payload: PipelineTransitionCreate, db: DbSession):
    try:
        return transition_pipeline(
            db,
            company_id=payload.company_id,
            opportunity_id=payload.opportunity_id,
            campaign_id=payload.campaign_id,
            to_state=payload.to_state,
            notes=payload.notes,
            metadata=payload.metadata,
            channel=payload.channel,
            contacted_at=payload.contacted_at,
            message_used=payload.message_used,
            expected_revenue=payload.expected_revenue,
            recurring_revenue_monthly=payload.recurring_revenue_monthly,
            implementation_revenue=payload.implementation_revenue,
            currency=payload.currency,
            closed_at=payload.closed_at,
            lost_reason=payload.lost_reason,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/analytics/funnel", response_model=FunnelAnalyticsRead)
def read_global_funnel(db: DbSession):
    return funnel_metrics(db)


@router.get("/campaigns/{campaign_id}/analytics", response_model=FunnelAnalyticsRead)
def read_campaign_funnel(campaign_id: int, db: DbSession):
    return funnel_metrics(db, campaign_id)


@router.get("/analytics/campaign-comparison", response_model=list[CampaignComparisonRead])
def read_campaign_comparison(db: DbSession):
    return campaign_comparison(db)


def _campaign_detail_response(
    db: Session, campaign: ProspectingCampaign
) -> ProspectingCampaignDetail:
    company_results: list[CampaignCompanyResult] = []
    for entry in campaign.companies:
        scores = [
            score
            for score in entry.company.opportunity_scores
            if score.opportunity_id == campaign.opportunity_id
        ]
        score = (
            sorted(scores, key=lambda item: item.total_score, reverse=True)[0] if scores else None
        )
        evidence_by_id = {item.id: item for item in entry.company.evidence}
        top_evidence = []
        if score is not None:
            top_evidence = [
                evidence_by_id[item_id]
                for item_id in score.evidence_ids
                if item_id in evidence_by_id
            ]
        company_results.append(
            CampaignCompanyResult(
                entry=entry,
                score=score,
                top_evidence=top_evidence,
                pipeline_state=current_pipeline_state(
                    db, entry.company_id, campaign.opportunity_id, campaign.id
                ),
            )
        )
    company_results.sort(
        key=lambda item: item.score.total_score if item.score is not None else -1, reverse=True
    )
    return ProspectingCampaignDetail(
        id=campaign.id,
        name=campaign.name,
        country=campaign.country,
        city_or_region=campaign.city_or_region,
        industries=campaign.industries,
        employee_min=campaign.employee_min,
        employee_max=campaign.employee_max,
        opportunity_id=campaign.opportunity_id,
        target_company_count=campaign.target_company_count,
        status=campaign.status,
        created_at=campaign.created_at,
        started_at=campaign.started_at,
        completed_at=campaign.completed_at,
        stats=campaign_stats(campaign),
        companies=company_results,
        research_runs=campaign.research_runs,
    )
