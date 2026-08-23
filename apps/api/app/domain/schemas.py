from datetime import datetime
from typing import Literal

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
    fingerprint: str
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
    research_runs: list["ResearchRunRead"] = Field(default_factory=list)


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


class FirstCustomerFitScoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
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
    first_customer_fit: FirstCustomerFitScoreRead | None = None
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
    diagnostics: dict
    created_at: datetime


class CampaignCompanyResult(BaseModel):
    entry: CampaignCompanyRead
    score: OpportunityScoreRead | None
    first_customer_fit: FirstCustomerFitScoreRead | None = None
    top_evidence: list[EvidenceRead]
    pipeline_state: str | None = None
    latest_research_run: ResearchRunRead | None = None


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
    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: int
    status: str
    operation: str
    message: str | None = None
    error: str | None = None
    started_at: datetime
    completed_at: datetime | None = None


class ContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    full_name: str | None
    role: str | None
    profile_url: str | None
    channel: str | None
    is_primary: bool
    notes: str | None
    created_at: datetime
    updated_at: datetime


class ContactUpsert(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
    role: str | None = Field(default=None, max_length=255)
    profile_url: str | None = Field(default=None, max_length=1024)
    channel: str | None = Field(default="LINKEDIN", max_length=40)
    notes: str | None = None


class CommercialNoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    contact_id: int | None
    opportunity_id: int | None
    body: str
    learning_tags: list[str]
    evidence_ids: list[int]
    created_at: datetime


DiscoveryOutcome = Literal[
    "NO_PROBLEM",
    "EXISTING_STACK_SOLVES_IT",
    "MEASURE_FIRST",
    "LABOR_CLOSE_CANDIDATE",
    "OUT_OF_SCOPE_WORK_CANDIDATE",
    "OTHER_WORKFLOW_SIGNAL",
    "PILOT_CANDIDATE",
    "DISQUALIFIED",
]
DiscoveryHypothesis = Literal[
    "PAYROLL_CLOSE_EXCEPTIONS",
    "OUT_OF_SCOPE_WORK",
    "OTHER_WORKFLOW",
]


class ReadinessDimension(BaseModel):
    score: int = Field(ge=0, le=2)
    reason: str = Field(min_length=1, max_length=1000)


class DiscoveryReadiness(BaseModel):
    pain_frequency: ReadinessDimension
    measurable_baseline: ReadinessDimension
    operational_consequence: ReadinessDimension
    existing_stack_gap: ReadinessDimension
    buyer_authority: ReadinessDimension
    workflow_owner_participation: ReadinessDimension
    implementation_simplicity: ReadinessDimension
    willingness_to_change: ReadinessDimension
    pilot_safety: ReadinessDimension
    repeatability: ReadinessDimension


class DiscoveryQualification(BaseModel):
    recurring_problem: bool | None = None
    usable_baseline: bool | None = None
    existing_stack_solves: bool | None = None
    sponsor_confirmed: bool | None = None
    workflow_owner_confirmed: bool | None = None
    bounded_safe_pilot: bool | None = None
    unsafe_requirement: bool = False
    out_of_scope_example_confirmed: bool | None = None


class DiscoveryMetrics(BaseModel):
    client_companies_payroll: int | None = Field(default=None, ge=0)
    employees_processed: int | None = Field(default=None, ge=0)
    portal_adoption_percent: float | None = Field(default=None, ge=0, le=100)
    companies_requiring_reminders: int | None = Field(default=None, ge=0)
    manual_reminders: int | None = Field(default=None, ge=0)
    minutes_per_reminder: float | None = Field(default=None, ge=0)
    total_followup_minutes: float | None = Field(default=None, ge=0)
    incomplete_at_cutoff: int | None = Field(default=None, ge=0)
    late_changes: int | None = Field(default=None, ge=0)
    corrections_reopens_last_quarter: int | None = Field(default=None, ge=0)
    people_involved: int | None = Field(default=None, ge=0)
    buyer_hourly_cost: float | None = Field(default=None, ge=0)
    out_of_scope_examples_90d: int | None = Field(default=None, ge=0)
    out_of_scope_estimated_value: float | None = Field(default=None, ge=0)
    out_of_scope_invoiced_value: float | None = Field(default=None, ge=0)
    invoice_delay_days: float | None = Field(default=None, ge=0)


class DiscoveryWorkflowDetails(BaseModel):
    cutoff: str | None = None
    portal: str | None = None
    real_client_channels: list[str] = Field(default_factory=list)
    spreadsheets_side_systems: list[str] = Field(default_factory=list)
    exception_owner: str | None = None
    status_visibility_method: str | None = None
    scope_check_method: str | None = None
    approval_owner: str | None = None
    work_before_pricing: bool | None = None
    out_of_scope_recording_method: str | None = None
    invoice_handoff: str | None = None
    profitability_review: str | None = None


class DiscoverySessionCreate(BaseModel):
    contact_id: int | None = None
    opportunity_id: int | None = None
    occurred_at: datetime
    hypothesis: DiscoveryHypothesis
    workflow_discussed: str = Field(min_length=1)
    discovery_status: Literal["COMPLETED", "PARTIAL", "FOLLOW_UP_REQUIRED"]
    existing_software: list[str] = Field(default_factory=list)
    workflow_details: DiscoveryWorkflowDetails = Field(default_factory=DiscoveryWorkflowDetails)
    buyer_reported_facts: list[str] = Field(default_factory=list)
    buyer_reported_metrics: DiscoveryMetrics = Field(default_factory=DiscoveryMetrics)
    pain_examples: list[str] = Field(default_factory=list)
    objections: list[str] = Field(default_factory=list)
    alternatives: list[str] = Field(default_factory=list)
    existing_stack_capability: Literal[
        "UNKNOWN",
        "SOLVES_WITH_REASONABLE_CONFIGURATION",
        "CONFIGURATION_GAP",
        "ADOPTION_GAP",
        "FUNCTIONALITY_GAP",
    ]
    qualification: DiscoveryQualification
    readiness: DiscoveryReadiness
    unresolved_questions: list[str] = Field(default_factory=list)
    next_action: str = Field(min_length=1)
    raw_notes: str | None = None


class DiscoverySessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    contact_id: int | None
    opportunity_id: int | None
    occurred_at: datetime
    hypothesis: DiscoveryHypothesis
    workflow_discussed: str
    discovery_status: str
    qualification_outcome: DiscoveryOutcome
    evidence_type: Literal["BUYER_REPORTED"]
    existing_software: list[str]
    workflow_details: dict
    buyer_reported_facts: list[str]
    buyer_reported_metrics: dict
    calculated_metrics: dict
    pain_examples: list[str]
    objections: list[str]
    alternatives: list[str]
    existing_stack_capability: str
    qualification: dict
    readiness: dict
    readiness_total: int
    fatal_blockers: list[str]
    unresolved_questions: list[str]
    missing_information: list[str]
    next_action: str
    raw_notes: str | None
    created_at: datetime


class CommercialScoreboardRead(BaseModel):
    connections_sent: int
    connections_accepted: int
    conversations_started: int
    discovery_calls: int
    no_problem: int
    existing_stack_solves_it: int
    measure_first: int
    payroll_candidates: int
    out_of_scope_candidates: int
    other_workflow_signals: int
    pilot_candidates: int
    disqualified: int
    pilots_proposed: int
    pilots_paid: int
    setup_revenue: float
    mrr: float
    north_star_mrr: float = 900
    next_objective: str = "FIRST_PAID_PILOT"


class CommercialActionCreate(BaseModel):
    action: str
    opportunity_id: int | None = None
    notes: str | None = None
    channel: str | None = "LINKEDIN"
    with_note: bool | None = None
    message_used: str | None = None
    message_version: str | None = Field(default=None, max_length=80)
    evidence_ids: list[int] = Field(default_factory=list)
    outreach_reason: str | None = None
    learning_tags: list[str] = Field(default_factory=list)
    lost_reason: str | None = Field(default=None, max_length=255)


class CommercialProspectRead(BaseModel):
    company: CompanyRead
    opportunity_id: int
    buyer: ContactRead | None
    status: str
    channel: str | None
    connection_note_used: str | None
    connection_note_type: str | None
    message_version: str | None
    selected_evidence: list[EvidenceRead]
    outreach_reason: str | None
    first_customer_fit: FirstCustomerFitScoreRead | None
    last_action: str
    last_action_at: datetime | None
    next_action: str
    contacted_at: datetime | None
    accepted_at: datetime | None
    replied_at: datetime | None
    meeting_at: datetime | None
    proposal_at: datetime | None
    closed_at: datetime | None
    lost_reason: str | None
    learning_tags: list[str]
    manual_notes: list[CommercialNoteRead]
    discovery_sessions: list[DiscoverySessionRead]


class OutreachTemplateRead(BaseModel):
    key: str
    label: str
    channel: str
    body: str
    placeholders: list[str]
    max_length: int | None = None
    automated: bool = False
