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
    campaign_id: int | None = None
    notes: str | None = None


class RankedOpportunityRead(BaseModel):
    score: OpportunityScoreRead
    company: CompanyRead
    top_evidence: list[EvidenceRead]
    why_matched: str
    pipeline_state: str | None = None
    latest_draft: OutreachDraftRead | None = None


class ProspectingCampaignCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    country: str = Field(min_length=1, max_length=120)
    city_or_region: str = Field(min_length=1, max_length=120)
    industries: list[str] = Field(min_length=1)
    employee_min: int | None = None
    employee_max: int | None = None
    opportunity_id: int = 1
    target_company_count: int = Field(default=20, ge=1, le=100)


class ProspectingCampaignRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    country: str
    city_or_region: str
    industries: list[str]
    employee_min: int | None
    employee_max: int | None
    opportunity_id: int
    target_company_count: int
    status: str
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None


class CampaignCompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    campaign_id: int
    company_id: int
    discovery_source: str
    discovery_metadata: dict
    research_state: str
    error: str | None
    company: CompanyRead


class ResearchRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    campaign_id: int | None
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    execution_time_ms: int
    status: str
    error: str | None
    created_at: datetime


class CampaignCompanyResult(BaseModel):
    entry: CampaignCompanyRead
    score: OpportunityScoreRead | None
    top_evidence: list[EvidenceRead]
    pipeline_state: str | None = None


class ProspectingCampaignDetail(ProspectingCampaignRead):
    stats: dict
    companies: list[CampaignCompanyResult]
    research_runs: list[ResearchRunRead]


class PipelineTransitionCreate(BaseModel):
    company_id: int
    opportunity_id: int
    campaign_id: int | None = None
    to_state: str
    notes: str | None = None
    metadata: dict = Field(default_factory=dict)
    channel: str | None = None
    contacted_at: datetime | None = None
    message_used: str | None = None
    expected_revenue: float | None = None
    recurring_revenue_monthly: float | None = None
    implementation_revenue: float | None = None
    currency: str | None = None
    closed_at: datetime | None = None
    lost_reason: str | None = None


class PipelineEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    campaign_id: int | None
    opportunity_id: int
    from_state: str | None
    to_state: str
    timestamp: datetime
    notes: str | None
    event_metadata: dict
    channel: str | None
    contacted_at: datetime | None
    message_used: str | None
    expected_revenue: float | None
    recurring_revenue_monthly: float | None
    implementation_revenue: float | None
    currency: str | None
    closed_at: datetime | None
    lost_reason: str | None


class CompanyTimelineRead(CompanyDetail):
    timeline: list[PipelineEventRead]


class FunnelAnalyticsRead(BaseModel):
    counts: dict
    conversion_rates: dict
    business_metrics: dict


class CampaignComparisonRead(BaseModel):
    campaign_id: int
    name: str
    sector: str
    companies_discovered: int
    qualified: int
    reply_rate: float
    meeting_rate: float
    win_rate: float
    revenue: float
    mrr: float
    research_cost: float


class ResearchJobRead(BaseModel):
    id: str
    company_id: int
    status: str
    operation: str
    message: str | None = None
    error: str | None = None
    started_at: datetime
    completed_at: datetime | None = None
