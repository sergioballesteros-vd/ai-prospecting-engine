"use client";

import {
  AlertCircle,
  Building2,
  CheckCircle2,
  FileSearch,
  Loader2,
  Play,
  Send,
  Search,
  Sparkles,
} from "lucide-react";
import Link from "next/link";
import { FormEvent, useEffect, useMemo, useState } from "react";
import {
  Analysis,
  Company,
  CompanyDetail,
  ResearchJob,
  createCompany,
  getCompany,
  getResearchJob,
  startResearch,
} from "@/lib/api";

export default function Home() {
  const [domain, setDomain] = useState("");
  const [company, setCompany] = useState<Company | null>(null);
  const [detail, setDetail] = useState<CompanyDetail | null>(null);
  const [job, setJob] = useState<ResearchJob | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const latestAnalysis = useMemo<Analysis | null>(() => {
    if (!detail?.analyses.length) return null;
    return [...detail.analyses].sort((a, b) => b.id - a.id)[0];
  }, [detail]);

  useEffect(() => {
    if (!job || job.status === "completed" || job.status === "failed") return;
    const interval = window.setInterval(async () => {
      try {
        const nextJob = await getResearchJob(job.id);
        setJob(nextJob);
        if (nextJob.status === "completed") {
          setDetail(await getCompany(nextJob.company_id));
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Could not refresh job state");
      }
    }, 1500);
    return () => window.clearInterval(interval);
  }, [job]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      const created = await createCompany(domain);
      setCompany(created);
      setDetail(await getCompany(created.id));
      const createdJob = await startResearch(created.id);
      setJob(createdJob);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Research could not be started");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand">
          <FileSearch size={22} />
          <span>AI Prospecting Engine</span>
        </div>
        <nav className="nav">
          <Link className="navItem active" href="/">
            <Search size={17} />
            Research
          </Link>
          <a className="navItem" href="#">
            <Building2 size={17} />
            Companies
          </a>
          <Link className="navItem" href="/campaigns">
            <Send size={17} />
            Campaigns
          </Link>
          <Link className="navItem" href="/opportunities">
            <Sparkles size={17} />
            Opportunities
          </Link>
        </nav>
        <div className="operator">
          <span className="avatar">SB</span>
          <span>
            <strong>Sergio Ballesteros</strong>
            <small>Internal workspace</small>
          </span>
        </div>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <h1>Research</h1>
            <p>Enter a company domain, extract public evidence, and review structured analysis.</p>
          </div>
          <span className="environment">No automatic outreach</span>
        </header>

        <form className="researchForm" onSubmit={submit}>
          <label>
            <span>Company domain</span>
            <input
              value={domain}
              onChange={(event) => setDomain(event.target.value)}
              placeholder="example.com"
              required
            />
          </label>
          <button type="submit" disabled={isSubmitting || !domain.trim()}>
            {isSubmitting ? <Loader2 className="spin" size={16} /> : <Play size={16} />}
            Run research
          </button>
        </form>

        {error ? (
          <div className="notice error">
            <AlertCircle size={16} />
            {error}
          </div>
        ) : null}

        <StatusStrip company={company} detail={detail} job={job} />

        <section className="split">
          <EvidencePanel detail={detail} />
          <AnalysisPanel analysis={latestAnalysis} job={job} />
        </section>
      </section>
    </main>
  );
}

function StatusStrip({
  company,
  detail,
  job,
}: {
  company: Company | null;
  detail: CompanyDetail | null;
  job: ResearchJob | null;
}) {
  const statusClass = job?.status === "failed" ? "failed" : job?.status === "completed" ? "done" : "live";
  return (
    <section className="statusStrip">
      <div>
        <span className="label">Company</span>
        <strong>{company ? company.name : "Not selected"}</strong>
      </div>
      <div>
        <span className="label">Latest job</span>
        <strong className={`status ${statusClass}`}>{job ? job.status : "idle"}</strong>
      </div>
      <div>
        <span className="label">Sources</span>
        <strong>{detail?.sources.length ?? 0}</strong>
      </div>
      <div>
        <span className="label">Evidence</span>
        <strong>{detail?.evidence.length ?? 0}</strong>
      </div>
      <div className="statusMessage">
        <span className="label">Message</span>
        <strong>{job?.error || job?.message || "Waiting for research"}</strong>
      </div>
    </section>
  );
}

function EvidencePanel({ detail }: { detail: CompanyDetail | null }) {
  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>Evidence</h2>
          <p>Signals are traceable to public source URLs.</p>
        </div>
        <span>{detail?.evidence.length ?? 0}</span>
      </div>
      <div className="evidenceList">
        {detail?.evidence.length ? (
          detail.evidence.map((item) => (
            <article className="evidenceRow" key={item.id}>
              <div>
                <div className="rowTitle">
                  <span>{item.signal_type}</span>
                  <small>{Math.round(item.confidence * 100)}%</small>
                </div>
                <p>{item.content_excerpt}</p>
                <a href={item.source_url} target="_blank" rel="noreferrer">
                  {item.source_url}
                </a>
              </div>
            </article>
          ))
        ) : (
          <EmptyState text="Run research to collect evidence." />
        )}
      </div>
    </section>
  );
}

function AnalysisPanel({ analysis, job }: { analysis: Analysis | null; job: ResearchJob | null }) {
  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>AI Analysis</h2>
          <p>Structured output, constrained to collected evidence.</p>
        </div>
        {job?.status === "running" ? <Loader2 className="spin" size={18} /> : null}
      </div>
      {analysis ? (
        <div className="analysis">
          <section>
            <h3>Summary</h3>
            <p>{analysis.summary}</p>
          </section>
          <section>
            <h3>Observed signals</h3>
            <ul>
              {analysis.observed_signals.map((signal) => (
                <li key={`${signal.signalType}-${signal.evidenceIds.join("-")}`}>
                  <CheckCircle2 size={15} />
                  <span>
                    <strong>{signal.signalType}</strong> {signal.reasoning}
                    <small>Evidence #{signal.evidenceIds.join(", #")}</small>
                  </span>
                </li>
              ))}
            </ul>
          </section>
          <section>
            <h3>Possible automation opportunities</h3>
            {analysis.possible_automation_opportunities.map((opportunity) => (
              <div className="opportunity" key={opportunity.problem}>
                <strong>{opportunity.problem}</strong>
                <p>{opportunity.reasoning}</p>
                <small>Evidence #{opportunity.evidenceIds.join(", #")}</small>
              </div>
            ))}
          </section>
          <section className="columns">
            <div>
              <h3>Unknowns</h3>
              {analysis.unknowns.map((unknown) => (
                <p key={unknown}>? {unknown}</p>
              ))}
            </div>
            <div>
              <h3>Buyer roles</h3>
              {analysis.recommended_buyer_roles.map((role) => (
                <p key={role}>{role}</p>
              ))}
            </div>
          </section>
        </div>
      ) : (
        <EmptyState text="Structured analysis will appear after evidence extraction." />
      )}
    </section>
  );
}

function EmptyState({ text }: { text: string }) {
  return <div className="empty">{text}</div>;
}
