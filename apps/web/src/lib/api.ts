const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api";

export type Company = {
  id: number;
  name: string;
  domain: string;
  website_url: string;
  industry: string | null;
  country: string | null;
  city: string | null;
  created_at: string;
};

export type Evidence = {
  id: number;
  company_id: number;
  source_id: number | null;
  signal_type: string;
  source_url: string;
  content_excerpt: string;
  fingerprint: string;
  confidence: number;
  detected_at: string;
  evidence_metadata: Record<string, unknown>;
};

export type ResearchDiagnostics = {
  pages_discovered?: number;
  pages_crawled?: number;
  pages_skipped?: number;
  evidence_extracted?: number;
  evidence_detected?: number;
  signals_detected?: number;
  crawl_failures?: number;
  content_bytes_collected?: number;
  content_tokens_estimated?: number;
  llm_input_tokens?: number;
  llm_output_tokens?: number;
  llm_cost?: number;
  total_research_latency_ms?: number;
  visited_pages?: Array<{
    url: string;
    reason: string;
    priority_score: number;
    status_code: number;
    content_bytes: number;
  }>;
  skipped_pages?: Array<{ url: string; reason: string }>;
  crawl_failure_details?: Array<{ url: string; error: string }>;
};

export type ResearchRun = {
  id: number;
  company_id: number;
  campaign_id: number | null;
  provider: string;
  model: string;
  input_tokens: number;
  output_tokens: number;
  estimated_cost: number;
  execution_time_ms: number;
  status: string;
  error: string | null;
  diagnostics: ResearchDiagnostics;
  created_at: string;
};

export type Analysis = {
  id: number;
  company_id: number;
  provider: string;
  model: string;
  summary: string;
  observed_signals: Array<{
    signalType: string;
    reasoning: string;
    confidence: number;
    evidenceIds: number[];
  }>;
  possible_automation_opportunities: Array<{
    problem: string;
    reasoning: string;
    confidence: number;
    evidenceIds: number[];
  }>;
  unknowns: string[];
  recommended_buyer_roles: string[];
  created_at: string;
};

export type CompanyDetail = Company & {
  sources: Array<{
    id: number;
    source_url: string;
    source_type: string;
    retrieved_at: string;
    source_metadata: Record<string, unknown>;
  }>;
  evidence: Evidence[];
  signals: Array<{
    id: number;
    signal_type: string;
    confidence: number;
    evidence_id: number;
  }>;
  analyses: Analysis[];
  research_runs: ResearchRun[];
};

export type ResearchJob = {
  id: string;
  company_id: number;
  status: "queued" | "running" | "completed" | "failed";
  operation: string;
  message: string | null;
  error: string | null;
  started_at: string;
  completed_at: string | null;
};

export type OpportunityScore = {
  id: number;
  company_id: number;
  opportunity_id: number;
  icp_score: number;
  pain_score: number;
  value_score: number;
  intent_score: number;
  reachability_score: number;
  confidence_score: number;
  total_score: number;
  qualification_state: "RESEARCHED" | "QUALIFIED" | "REJECTED" | "APPROVED";
  explanation: string;
  evidence_ids: number[];
  matched_signals: string[];
  created_at: string;
  updated_at: string;
};

export type FirstCustomerFitScore = {
  id: number;
  company_id: number;
  size_fit: number;
  buyer_accessibility: number;
  workflow_fit: number;
  automation_gap: number;
  sales_simplicity: number;
  implementation_fit: number;
  confidence: number;
  total_score: number;
  positive_reasons: string[];
  negative_reasons: string[];
  disqualifiers: string[];
  evidence_ids: number[];
  matched_signals: string[];
  explanation: string;
  created_at: string;
  updated_at: string;
};

export type OutreachDraft = {
  id: number;
  company_id: number;
  opportunity_id: number;
  opportunity_score_id: number | null;
  channel: string;
  subject: string;
  body: string;
  evidence_used: number[];
  status: "DRAFT" | "READY_FOR_REVIEW";
  created_at: string;
  updated_at: string;
};

export type PipelineState =
  | "APPROVED"
  | "CONTACTED"
  | "CONNECTION_SENT"
  | "ACCEPTED"
  | "REPLIED"
  | "MEETING"
  | "PROPOSAL"
  | "WON"
  | "LOST";

export type PipelineEvent = {
  id: number;
  company_id: number;
  campaign_id: number | null;
  opportunity_id: number;
  from_state: PipelineState | null;
  to_state: PipelineState;
  timestamp: string;
  notes: string | null;
  event_metadata: Record<string, unknown>;
  channel: "EMAIL" | "LINKEDIN" | "PHONE" | "OTHER" | null;
  contacted_at: string | null;
  message_used: string | null;
  expected_revenue: number | null;
  recurring_revenue_monthly: number | null;
  implementation_revenue: number | null;
  currency: string | null;
  closed_at: string | null;
  lost_reason: string | null;
};

export type RankedOpportunity = {
  score: OpportunityScore;
  first_customer_fit: FirstCustomerFitScore | null;
  company: Company;
  top_evidence: Evidence[];
  why_matched: string;
  pipeline_state: PipelineState | null;
  latest_draft: OutreachDraft | null;
};

export type ProspectingCampaign = {
  id: number;
  name: string;
  country: string;
  city_or_region: string;
  industries: string[];
  employee_min: number | null;
  employee_max: number | null;
  opportunity_id: number;
  target_company_count: number;
  status: "DRAFT" | "RUNNING" | "COMPLETED" | "FAILED";
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
};

export type CampaignCompanyResult = {
  entry: {
    id: number;
    campaign_id: number;
    company_id: number;
    discovery_source: string;
    discovery_metadata: Record<string, unknown>;
    research_state: "DISCOVERED" | "RESEARCHING" | "RESEARCHED" | "FAILED";
    error: string | null;
    company: Company;
  };
  score: OpportunityScore | null;
  first_customer_fit: FirstCustomerFitScore | null;
  top_evidence: Evidence[];
  pipeline_state: PipelineState | null;
  latest_research_run: ResearchRun | null;
};

export type Contact = {
  id: number;
  company_id: number;
  full_name: string | null;
  role: string | null;
  profile_url: string | null;
  channel: string | null;
  is_primary: boolean;
  notes: string | null;
  created_at: string;
  updated_at: string;
};

export type CommercialNote = {
  id: number;
  company_id: number;
  contact_id: number | null;
  opportunity_id: number | null;
  body: string;
  learning_tags: string[];
  evidence_ids: number[];
  created_at: string;
};

export type DiscoveryOutcome =
  | "NO_PROBLEM"
  | "EXISTING_STACK_SOLVES_IT"
  | "MEASURE_FIRST"
  | "LABOR_CLOSE_CANDIDATE"
  | "OUT_OF_SCOPE_WORK_CANDIDATE"
  | "OTHER_WORKFLOW_SIGNAL"
  | "PILOT_CANDIDATE"
  | "DISQUALIFIED";

export type DiscoveryHypothesis =
  | "PAYROLL_CLOSE_EXCEPTIONS"
  | "OUT_OF_SCOPE_WORK"
  | "OTHER_WORKFLOW";

export type ReadinessDimension = { score: 0 | 1 | 2; reason: string };

export type DiscoverySession = {
  id: number;
  company_id: number;
  contact_id: number | null;
  opportunity_id: number | null;
  occurred_at: string;
  hypothesis: DiscoveryHypothesis;
  workflow_discussed: string;
  discovery_status: "COMPLETED" | "PARTIAL" | "FOLLOW_UP_REQUIRED";
  qualification_outcome: DiscoveryOutcome;
  evidence_type: "BUYER_REPORTED";
  existing_software: string[];
  workflow_details: Record<string, string | boolean | string[] | null>;
  buyer_reported_facts: string[];
  buyer_reported_metrics: Record<string, number>;
  calculated_metrics: Record<
    string,
    { value: number; unit: string; formula: string; source_fields: string[] }
  >;
  pain_examples: string[];
  objections: string[];
  alternatives: string[];
  existing_stack_capability: string;
  qualification: Record<string, boolean | null>;
  readiness: Record<string, ReadinessDimension>;
  readiness_total: number;
  fatal_blockers: string[];
  unresolved_questions: string[];
  missing_information: string[];
  next_action: string;
  raw_notes: string | null;
  created_at: string;
};

export type DiscoverySessionPayload = Omit<
  DiscoverySession,
  | "id"
  | "company_id"
  | "qualification_outcome"
  | "evidence_type"
  | "calculated_metrics"
  | "readiness_total"
  | "fatal_blockers"
  | "missing_information"
  | "created_at"
>;

export type CommercialScoreboard = {
  connections_sent: number;
  connections_accepted: number;
  conversations_started: number;
  discovery_calls: number;
  no_problem: number;
  existing_stack_solves_it: number;
  measure_first: number;
  payroll_candidates: number;
  out_of_scope_candidates: number;
  other_workflow_signals: number;
  pilot_candidates: number;
  disqualified: number;
  pilots_proposed: number;
  pilots_paid: number;
  setup_revenue: number;
  mrr: number;
  north_star_mrr: number;
  next_objective: "FIRST_PAID_PILOT";
};

export type CommercialStatus =
  | "TO_CONTACT"
  | "CONNECTION_SENT"
  | "ACCEPTED"
  | "REPLIED"
  | "MEETING"
  | "PROPOSAL"
  | "WON"
  | "LOST";

export type CommercialProspect = {
  company: Company;
  opportunity_id: number;
  buyer: Contact | null;
  status: CommercialStatus;
  channel: string | null;
  connection_note_used: string | null;
  connection_note_type: "WITH_NOTE" | "WITHOUT_NOTE" | null;
  message_version: string | null;
  selected_evidence: Evidence[];
  outreach_reason: string | null;
  first_customer_fit: FirstCustomerFitScore | null;
  last_action: string;
  last_action_at: string | null;
  next_action: string;
  contacted_at: string | null;
  accepted_at: string | null;
  replied_at: string | null;
  meeting_at: string | null;
  proposal_at: string | null;
  closed_at: string | null;
  lost_reason: string | null;
  learning_tags: string[];
  manual_notes: CommercialNote[];
  discovery_sessions: DiscoverySession[];
};

export type CommercialAction =
  | "MARK_CONNECTION_SENT"
  | "MARK_ACCEPTED"
  | "MARK_REPLIED"
  | "MARK_MEETING"
  | "MARK_REJECTED"
  | "MARK_NO_RESPONSE"
  | "ADD_NOTE";

export type OutreachTemplate = {
  key: string;
  label: string;
  channel: string;
  body: string;
  placeholders: string[];
  max_length: number | null;
  automated: false;
};

export type ProspectingCampaignDetail = ProspectingCampaign & {
  stats: {
    discovered: number;
    target: number;
    researched: number;
    failed: number;
    qualified: number;
    approved: number;
    total_research_cost: number;
    average_cost_per_company: number;
  };
  companies: CampaignCompanyResult[];
  research_runs: ResearchRun[];
};

export type CompanyTimeline = CompanyDetail & {
  timeline: PipelineEvent[];
};

export type FunnelAnalytics = {
  counts: Record<
    | "discovered"
    | "researched"
    | "qualified"
    | "approved"
    | "contacted"
    | "replied"
    | "meetings"
    | "proposals"
    | "won"
    | "lost",
    number
  >;
  conversion_rates: Record<
    "contacted_to_reply" | "reply_to_meeting" | "meeting_to_proposal" | "proposal_to_won",
    number
  >;
  business_metrics: Record<
    | "revenue_generated"
    | "mrr_generated"
    | "average_deal_value"
    | "revenue_per_100_discovered"
    | "revenue_per_100_contacted"
    | "research_cost_per_meeting"
    | "research_cost_per_won_customer"
    | "research_cost",
    number
  >;
};

export type CampaignComparison = {
  campaign_id: number;
  name: string;
  sector: string;
  companies_discovered: number;
  qualified: number;
  reply_rate: number;
  meeting_rate: number;
  win_rate: number;
  revenue: number;
  mrr: number;
  research_cost: number;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function createCompany(domain: string): Promise<Company> {
  return request<Company>("/companies", {
    method: "POST",
    body: JSON.stringify({ domain }),
  });
}

export function startResearch(companyId: number): Promise<ResearchJob> {
  return request<ResearchJob>(`/companies/${companyId}/research`, { method: "POST" });
}

export function getResearchJob(jobId: string): Promise<ResearchJob> {
  return request<ResearchJob>(`/research-jobs/${jobId}`);
}

export function getCompany(companyId: number): Promise<CompanyDetail> {
  return request<CompanyDetail>(`/companies/${companyId}`);
}

export function listCompanies(): Promise<Company[]> {
  return request<Company[]>("/companies");
}

export function listRankedOpportunities(): Promise<RankedOpportunity[]> {
  return request<RankedOpportunity[]>("/opportunities/ranked");
}

export function updateOpportunityState(
  scoreId: number,
  state: OpportunityScore["qualification_state"],
): Promise<RankedOpportunity> {
  return request<RankedOpportunity>(`/opportunity-scores/${scoreId}/state`, {
    method: "PATCH",
    body: JSON.stringify({ state }),
  });
}

export function createPipelineEvent(payload: {
  company_id: number;
  opportunity_id: number;
  campaign_id?: number | null;
  to_state: PipelineState;
  notes?: string | null;
  metadata?: Record<string, unknown>;
  channel?: PipelineEvent["channel"];
  contacted_at?: string | null;
  message_used?: string | null;
  expected_revenue?: number | null;
  recurring_revenue_monthly?: number | null;
  implementation_revenue?: number | null;
  currency?: string | null;
  closed_at?: string | null;
  lost_reason?: string | null;
}): Promise<PipelineEvent> {
  return request<PipelineEvent>("/pipeline/events", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getCompanyTimeline(companyId: number): Promise<CompanyTimeline> {
  return request<CompanyTimeline>(`/companies/${companyId}/timeline`);
}

export function getGlobalFunnel(): Promise<FunnelAnalytics> {
  return request<FunnelAnalytics>("/analytics/funnel");
}

export function getCampaignAnalytics(campaignId: number): Promise<FunnelAnalytics> {
  return request<FunnelAnalytics>(`/campaigns/${campaignId}/analytics`);
}

export function getCampaignComparison(): Promise<CampaignComparison[]> {
  return request<CampaignComparison[]>("/analytics/campaign-comparison");
}

export function generateDraft(scoreId: number): Promise<OutreachDraft> {
  return request<OutreachDraft>(`/opportunity-scores/${scoreId}/draft`, { method: "POST" });
}

export function updateDraft(
  draftId: number,
  payload: Pick<OutreachDraft, "subject" | "body" | "status">,
): Promise<OutreachDraft> {
  return request<OutreachDraft>(`/outreach-drafts/${draftId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function listCampaigns(): Promise<ProspectingCampaign[]> {
  return request<ProspectingCampaign[]>("/campaigns");
}

export function createCampaign(payload: {
  name: string;
  country: string;
  city_or_region: string;
  industries: string[];
  employee_min: number | null;
  employee_max: number | null;
  opportunity_id: number;
  target_company_count: number;
}): Promise<ProspectingCampaign> {
  return request<ProspectingCampaign>("/campaigns", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getCampaign(campaignId: number): Promise<ProspectingCampaignDetail> {
  return request<ProspectingCampaignDetail>(`/campaigns/${campaignId}`);
}

export function runCampaign(campaignId: number): Promise<ProspectingCampaign> {
  return request<ProspectingCampaign>(`/campaigns/${campaignId}/run`, { method: "POST" });
}

export function retryCampaignCompany(entryId: number): Promise<CampaignCompanyResult["entry"]> {
  return request<CampaignCompanyResult["entry"]>(`/campaign-companies/${entryId}/retry`, {
    method: "POST",
  });
}

export function listCommercialProspects(): Promise<CommercialProspect[]> {
  return request<CommercialProspect[]>("/commercial/prospects");
}

export function getCommercialScoreboard(): Promise<CommercialScoreboard> {
  return request<CommercialScoreboard>("/commercial/scoreboard");
}

export function createDiscoverySession(
  companyId: number,
  payload: DiscoverySessionPayload,
): Promise<DiscoverySession> {
  return request<DiscoverySession>(`/commercial/prospects/${companyId}/discovery-sessions`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function saveCommercialBuyer(
  companyId: number,
  payload: {
    full_name: string | null;
    role: string | null;
    profile_url: string | null;
    channel?: string | null;
    notes?: string | null;
  },
): Promise<Contact> {
  return request<Contact>(`/commercial/prospects/${companyId}/buyer`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export function recordCommercialAction(
  companyId: number,
  payload: {
    action: CommercialAction;
    opportunity_id?: number | null;
    notes?: string | null;
    channel?: string | null;
    with_note?: boolean | null;
    message_used?: string | null;
    message_version?: string | null;
    evidence_ids?: number[];
    outreach_reason?: string | null;
    learning_tags?: string[];
    lost_reason?: string | null;
  },
): Promise<CommercialProspect> {
  return request<CommercialProspect>(`/commercial/prospects/${companyId}/actions`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function listOutreachTemplates(): Promise<OutreachTemplate[]> {
  return request<OutreachTemplate[]>("/commercial/templates");
}
