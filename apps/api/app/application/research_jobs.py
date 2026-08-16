import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from time import perf_counter
from uuid import uuid4

from sqlalchemy.orm import Session

from app.application.opportunity_review import default_opportunity, upsert_opportunity_score
from app.domain.models import (
    Company,
    CompanyAnalysis,
    CompanySignal,
    CompanySource,
    Evidence,
    ResearchRun,
)
from app.infrastructure.database import SessionLocal
from app.infrastructure.settings import get_settings
from app.modules.research.llm import provider_from_settings
from app.modules.research.website import detect_evidence, extract_relevant_pages

logger = logging.getLogger(__name__)


@dataclass
class ResearchJob:
    id: str
    company_id: int
    status: str
    operation: str
    started_at: datetime
    completed_at: datetime | None = None
    message: str | None = None
    error: str | None = None


JOBS: dict[str, ResearchJob] = {}


def create_research_job(company_id: int) -> ResearchJob:
    job = ResearchJob(
        id=str(uuid4()),
        company_id=company_id,
        status="queued",
        operation="RESEARCH_COMPANY",
        started_at=datetime.now(UTC),
        message="Research queued",
    )
    JOBS[job.id] = job
    return job


def get_research_job(job_id: str) -> ResearchJob | None:
    return JOBS.get(job_id)


async def run_research_job(job_id: str) -> None:
    job = JOBS[job_id]
    job.status = "running"
    job.message = "Fetching website pages"
    started = datetime.now(UTC)
    db = SessionLocal()
    try:
        await _research_company(db, job)
        job.status = "completed"
        job.message = "Research completed"
    except Exception as exc:
        logger.exception(
            "research_job_failed",
            extra={"job_id": job.id, "company_id": job.company_id, "operation": job.operation},
        )
        job.status = "failed"
        job.error = str(exc)
        job.message = "Research failed"
    finally:
        db.close()
        job.completed_at = datetime.now(UTC)
        logger.info(
            "research_job_finished",
            extra={
                "job_id": job.id,
                "company_id": job.company_id,
                "operation": job.operation,
                "duration_seconds": (job.completed_at - started).total_seconds(),
                "status": job.status,
            },
        )


async def _research_company(db: Session, job: ResearchJob) -> None:
    await research_company(db, job.company_id)


async def research_company(db: Session, company_id: int, campaign_id: int | None = None) -> None:
    started = perf_counter()
    company = db.get(Company, company_id)
    if company is None:
        raise ValueError("Company not found")

    pages = await extract_relevant_pages(company.domain)

    sources_by_url: dict[str, CompanySource] = {}
    for page in pages:
        source = CompanySource(
            company_id=company.id,
            source_type="website_page",
            source_url=page.url,
            source_metadata={"title": page.title, "status_code": page.status_code},
        )
        db.add(source)
        db.flush()
        sources_by_url[page.url] = source

    detected = detect_evidence(pages)
    evidence_rows: list[Evidence] = []
    for item in detected:
        source = sources_by_url.get(item.source_url)
        evidence = Evidence(
            company_id=company.id,
            source_id=source.id if source else None,
            signal_type=item.signal_type,
            source_url=item.source_url,
            content_excerpt=item.content_excerpt,
            confidence=item.confidence,
            evidence_metadata=item.metadata,
        )
        db.add(evidence)
        db.flush()
        db.add(
            CompanySignal(
                company_id=company.id,
                signal_type=item.signal_type,
                confidence=item.confidence,
                evidence_id=evidence.id,
            )
        )
        evidence_rows.append(evidence)
    db.commit()

    provider = provider_from_settings(get_settings())
    analysis = await provider.analyze_company(company, evidence_rows)
    _validate_analysis_references(analysis.model_dump(), {item.id for item in evidence_rows})
    db.add(
        CompanyAnalysis(
            company_id=company.id,
            provider=provider.provider_name,
            model=provider.model_name,
            summary=analysis.summary,
            observed_signals=[item.model_dump() for item in analysis.observedSignals],
            possible_automation_opportunities=[
                item.model_dump() for item in analysis.possibleAutomationOpportunities
            ],
            unknowns=analysis.unknowns,
            recommended_buyer_roles=analysis.recommendedBuyerRoles,
            raw_output=analysis.model_dump(),
        )
    )
    upsert_opportunity_score(db, company, default_opportunity(db))
    usage = _estimate_research_usage(
        provider.provider_name, provider.model_name, evidence_rows, analysis
    )
    db.add(
        ResearchRun(
            company_id=company.id,
            campaign_id=campaign_id,
            provider=provider.provider_name,
            model=provider.model_name,
            input_tokens=usage["input_tokens"],
            output_tokens=usage["output_tokens"],
            estimated_cost=usage["estimated_cost"],
            execution_time_ms=int((perf_counter() - started) * 1000),
            status="COMPLETED",
        )
    )
    db.commit()


def _validate_analysis_references(payload: dict, evidence_ids: set[int]) -> None:
    for collection in ("observedSignals", "possibleAutomationOpportunities"):
        for item in payload.get(collection, []):
            ids = set(item.get("evidenceIds", []))
            if not ids.issubset(evidence_ids):
                unknown_ids = sorted(ids - evidence_ids)
                raise ValueError(f"Analysis referenced unknown evidence ids: {unknown_ids}")


def schedule_background_job(job_id: str) -> None:
    asyncio.create_task(run_research_job(job_id))


def _estimate_research_usage(
    provider: str, model: str, evidence: list[Evidence], analysis: object
) -> dict[str, int | float]:
    input_chars = sum(len(item.content_excerpt) for item in evidence)
    output_chars = len(json.dumps(analysis.model_dump(), default=str))
    input_tokens = max(0, input_chars // 4)
    output_tokens = max(0, output_chars // 4)
    if provider != "openai":
        return {"input_tokens": input_tokens, "output_tokens": output_tokens, "estimated_cost": 0.0}
    rate = 0.0000004 if "mini" in model else 0.000002
    estimated_cost = round((input_tokens + output_tokens) * rate, 6)
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost": estimated_cost,
    }
