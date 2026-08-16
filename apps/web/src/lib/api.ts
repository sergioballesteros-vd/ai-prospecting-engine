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
