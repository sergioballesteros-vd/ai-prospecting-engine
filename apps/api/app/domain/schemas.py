from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CompanyCreate(BaseModel):
    domain: str = Field(min_length=3, max_length=255)
    name: str | None = Field(default=None, max_length=255)
    country: str | None = None
    city: str | None = None
    industry: str | None = None


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    domain: str
    website_url: str
    industry: str | None
    country: str | None
    city: str | None
    created_at: datetime


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    source_type: str
    source_url: str
    retrieved_at: datetime
    source_metadata: dict


class EvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    source_id: int | None
    signal_type: str
    source_url: str
    content_excerpt: str
    confidence: float
    detected_at: datetime
    evidence_metadata: dict


class SignalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    signal_type: str
    confidence: float
    evidence_id: int
    created_at: datetime


class AnalysisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    provider: str
    model: str
    summary: str
    observed_signals: list[dict]
    possible_automation_opportunities: list[dict]
    unknowns: list[str]
    recommended_buyer_roles: list[str]
    created_at: datetime


class CompanyDetail(CompanyRead):
    sources: list[SourceRead]
    evidence: list[EvidenceRead]
    signals: list[SignalRead]
    analyses: list[AnalysisRead]


class ResearchJobRead(BaseModel):
    id: str
    company_id: int
    status: str
    operation: str
    message: str | None = None
    error: str | None = None
    started_at: datetime
    completed_at: datetime | None = None
