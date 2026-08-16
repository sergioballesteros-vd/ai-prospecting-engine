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


class OpportunityScoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    opportunity_id: int
    icp_score: float
    pain_score: float
    value_score: float
    intent_score: float
    reachability_score: float
    confidence_score: float
    total_score: float
    qualification_state: str
    explanation: str
    evidence_ids: list[int]
    matched_signals: list[str]
    created_at: datetime
    updated_at: datetime


class OutreachDraftRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    opportunity_id: int
    opportunity_score_id: int | None
    channel: str
    subject: str
    body: str
    evidence_used: list[int]
    status: str
    created_at: datetime
    updated_at: datetime


class OutreachDraftUpdate(BaseModel):
    subject: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1)
    status: str | None = None


class ReviewStateUpdate(BaseModel):
    state: str


class RankedOpportunityRead(BaseModel):
    score: OpportunityScoreRead
    company: CompanyRead
    top_evidence: list[EvidenceRead]
    why_matched: str
    latest_draft: OutreachDraftRead | None = None


class ResearchJobRead(BaseModel):
    id: str
    company_id: int
    status: str
    operation: str
    message: str | None = None
    error: str | None = None
    started_at: datetime
    completed_at: datetime | None = None
