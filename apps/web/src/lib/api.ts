const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

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
  confidence: number;
  detected_at: string;
  evidence_metadata: Record<string, unknown>;
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

export type RankedOpportunity = {
  score: OpportunityScore;
  company: Company;
  top_evidence: Evidence[];
  why_matched: string;
  latest_draft: OutreachDraft | null;
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
