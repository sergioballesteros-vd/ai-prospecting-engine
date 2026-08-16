from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.application.research_jobs import create_research_job, get_research_job, run_research_job
from app.domain.models import Company
from app.domain.schemas import CompanyCreate, CompanyDetail, CompanyRead, ResearchJobRead
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
        )
    )
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/companies/{company_id}/research", response_model=ResearchJobRead)
def start_research(company_id: int, background_tasks: BackgroundTasks, db: DbSession):
    if db.get(Company, company_id) is None:
        raise HTTPException(status_code=404, detail="Company not found")
    job = create_research_job(company_id)
    background_tasks.add_task(run_research_job, job.id)
    return job


@router.get("/research-jobs/{job_id}", response_model=ResearchJobRead)
def read_research_job(job_id: str):
    job = get_research_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Research job not found")
    return job
