import logging
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.application.opportunity_review import upsert_opportunity_score
from app.application.research_jobs import research_company
from app.domain.models import (
    CampaignCompany,
    Company,
    CompanySource,
    Opportunity,
    ProspectingCampaign,
    ResearchRun,
)
from app.infrastructure.database import SessionLocal
from app.infrastructure.settings import get_settings
from app.modules.discovery.providers import (
    CompanyCandidate,
    CompanyDiscoveryProvider,
    DiscoveryCriteria,
    provider_from_settings,
)
from app.modules.research.website import normalize_domain, website_url_for_domain

logger = logging.getLogger(__name__)
CAMPAIGN_STATUSES = {"DRAFT", "RUNNING", "COMPLETED", "FAILED"}


def create_campaign(
    db: Session,
    *,
    name: str,
    country: str,
    city_or_region: str,
    industries: list[str],
    employee_min: int | None,
    employee_max: int | None,
    opportunity_id: int,
    target_company_count: int,
) -> ProspectingCampaign:
    if db.get(Opportunity, opportunity_id) is None:
        raise ValueError("Opportunity not found")
    campaign = ProspectingCampaign(
        name=name,
        country=country,
        city_or_region=city_or_region,
        industries=industries,
        employee_min=employee_min,
        employee_max=employee_max,
        opportunity_id=opportunity_id,
        target_company_count=target_company_count,
        status="DRAFT",
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


async def run_campaign(campaign_id: int, provider: CompanyDiscoveryProvider | None = None) -> None:
    db = SessionLocal()
    try:
        campaign = db.get(ProspectingCampaign, campaign_id)
        if campaign is None:
            raise ValueError("Campaign not found")
        campaign.status = "RUNNING"
        campaign.started_at = datetime.now(UTC)
        campaign.completed_at = None
        db.commit()

        discovery_provider = provider or provider_from_settings(get_settings())
        criteria = DiscoveryCriteria(
            country=campaign.country,
            city_or_region=campaign.city_or_region,
            industries=campaign.industries,
            employee_min=campaign.employee_min,
            employee_max=campaign.employee_max,
            target_company_count=campaign.target_company_count,
        )
        candidates = await discovery_provider.discover(criteria)
        entries = _persist_candidates(db, campaign, candidates)
        for entry in entries:
            await _research_campaign_company(db, campaign, entry)

        campaign.status = "COMPLETED"
        campaign.completed_at = datetime.now(UTC)
        db.commit()
    except Exception:
        logger.exception("campaign_failed", extra={"campaign_id": campaign_id})
        campaign = db.get(ProspectingCampaign, campaign_id)
        if campaign is not None:
            campaign.status = "FAILED"
            campaign.completed_at = datetime.now(UTC)
            db.commit()
    finally:
        db.close()


def campaign_detail(db: Session, campaign_id: int) -> ProspectingCampaign:
    campaign = db.scalar(
        select(ProspectingCampaign)
        .where(ProspectingCampaign.id == campaign_id)
        .options(
            selectinload(ProspectingCampaign.companies)
            .selectinload(CampaignCompany.company)
            .selectinload(Company.evidence),
            selectinload(ProspectingCampaign.companies)
            .selectinload(CampaignCompany.company)
            .selectinload(Company.opportunity_scores),
            selectinload(ProspectingCampaign.research_runs),
        )
    )
    if campaign is None:
        raise ValueError("Campaign not found")
    return campaign


def campaign_stats(campaign: ProspectingCampaign) -> dict[str, int | float]:
    entries = campaign.companies
    discovered = len(entries)
    researched = sum(1 for entry in entries if entry.research_state == "RESEARCHED")
    failed = sum(1 for entry in entries if entry.research_state == "FAILED")
    qualified = 0
    approved = 0
    for entry in entries:
        for score in entry.company.opportunity_scores:
            if score.opportunity_id != campaign.opportunity_id:
                continue
            qualified += int(score.qualification_state in {"QUALIFIED", "APPROVED"})
            approved += int(score.qualification_state == "APPROVED")
    total_cost = sum(run.estimated_cost for run in campaign.research_runs)
    average_cost = total_cost / researched if researched else 0
    return {
        "discovered": discovered,
        "target": campaign.target_company_count,
        "researched": researched,
        "failed": failed,
        "qualified": qualified,
        "approved": approved,
        "total_research_cost": round(total_cost, 6),
        "average_cost_per_company": round(average_cost, 6),
    }


async def retry_campaign_company(db: Session, entry_id: int) -> CampaignCompany:
    entry = db.get(CampaignCompany, entry_id)
    if entry is None:
        raise ValueError("Campaign company not found")
    campaign = entry.campaign
    await _research_campaign_company(db, campaign, entry)
    db.refresh(entry)
    return entry


def _persist_candidates(
    db: Session, campaign: ProspectingCampaign, candidates: list[CompanyCandidate]
) -> list[CampaignCompany]:
    entries: list[CampaignCompany] = []
    seen_domains: set[str] = set()
    for candidate in candidates:
        domain = _candidate_domain(candidate)
        if domain is None or domain in seen_domains:
            continue
        seen_domains.add(domain)
        company = db.scalar(select(Company).where(Company.domain == domain))
        if company is None:
            company = Company(
                name=candidate.name,
                domain=domain,
                website_url=candidate.website_url or website_url_for_domain(domain),
                industry=candidate.industry,
                country=candidate.country,
                city=candidate.city,
            )
            db.add(company)
            db.flush()
        db.add(
            CompanySource(
                company_id=company.id,
                source_type=f"discovery:{candidate.source}",
                source_url=candidate.source_url,
                source_metadata=candidate.metadata,
            )
        )
        existing_entry = db.scalar(
            select(CampaignCompany).where(
                CampaignCompany.campaign_id == campaign.id,
                CampaignCompany.company_id == company.id,
            )
        )
        if existing_entry is not None:
            entries.append(existing_entry)
            continue
        entry = CampaignCompany(
            campaign_id=campaign.id,
            company_id=company.id,
            discovery_source=candidate.source,
            discovery_metadata=candidate.metadata,
            research_state="DISCOVERED",
        )
        db.add(entry)
        db.flush()
        entries.append(entry)
        if len(entries) >= campaign.target_company_count:
            break
    db.commit()
    return entries


async def _research_campaign_company(
    db: Session, campaign: ProspectingCampaign, entry: CampaignCompany
) -> None:
    entry.research_state = "RESEARCHING"
    entry.error = None
    entry.updated_at = datetime.now(UTC)
    db.commit()
    try:
        company = db.get(Company, entry.company_id)
        if company is None:
            raise ValueError("Company not found")
        await research_company(db, company.id, campaign.id)
        upsert_opportunity_score(db, company, campaign.opportunity)
        entry.research_state = "RESEARCHED"
        entry.updated_at = datetime.now(UTC)
        db.commit()
    except Exception as exc:
        db.rollback()
        entry = db.get(CampaignCompany, entry.id)
        if entry is not None:
            entry.research_state = "FAILED"
            entry.error = str(exc)
            entry.updated_at = datetime.now(UTC)
        if entry is not None:
            db.add(
                ResearchRun(
                    company_id=entry.company_id,
                    campaign_id=campaign.id,
                    provider="research",
                    model="unknown",
                    input_tokens=0,
                    output_tokens=0,
                    estimated_cost=0,
                    execution_time_ms=0,
                    status="FAILED",
                    error=str(exc),
                    diagnostics={"crawl_failures": 1, "error": str(exc)},
                )
            )
        db.commit()


def _candidate_domain(candidate: CompanyCandidate) -> str | None:
    value = candidate.domain or candidate.website_url
    if not value:
        return None
    try:
        return normalize_domain(value)
    except ValueError:
        return None
