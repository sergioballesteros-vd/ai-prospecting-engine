"use client";

import { FileSearch, RefreshCw, Search, Send, Sparkles } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import {
  CampaignCompanyResult,
  ProspectingCampaignDetail,
  getCampaign,
  retryCampaignCompany,
  runCampaign,
} from "@/lib/api";

export default function CampaignDetailPage() {
  const params = useParams<{ id: string }>();
  const campaignId = Number(params.id);
  const [campaign, setCampaign] = useState<ProspectingCampaignDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      setCampaign(await getCampaign(campaignId));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load campaign");
    }
  }, [campaignId]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  useEffect(() => {
    if (campaign?.status !== "RUNNING") return;
    const timer = window.setInterval(refresh, 2000);
    return () => window.clearInterval(timer);
  }, [campaign?.status, refresh]);

  async function start() {
    setPending("run");
    setError(null);
    try {
      await runCampaign(campaignId);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not run campaign");
    } finally {
      setPending(null);
    }
  }

  async function retry(entryId: number) {
    setPending(`retry-${entryId}`);
    try {
      await retryCampaignCompany(entryId);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Retry failed");
    } finally {
      setPending(null);
    }
  }

  if (!campaign) {
    return <div className="empty">Loading campaign...</div>;
  }

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand">
          <FileSearch size={22} />
          <span>AI Prospecting Engine</span>
        </div>
        <nav className="nav">
          <Link className="navItem" href="/">
            <Search size={17} />
            Research
          </Link>
          <Link className="navItem active" href="/campaigns">
            <Send size={17} />
            Campaigns
          </Link>
          <Link className="navItem" href="/opportunities">
            <Sparkles size={17} />
            Opportunities
          </Link>
        </nav>
      </aside>
      <section className="workspace">
        <header className="topbar">
          <div>
            <h1>{campaign.name}</h1>
            <p>
              {campaign.city_or_region}, {campaign.country} · {campaign.industries.join(", ")}
            </p>
          </div>
          <button className="secondaryButton" onClick={start} disabled={pending === "run"}>
            <RefreshCw size={16} />
            {campaign.status === "DRAFT" ? "Run campaign" : "Run again"}
          </button>
        </header>
        {error ? <div className="notice error">{error}</div> : null}
        <section className="campaignStats">
          <Stat label="Discovered" value={`${campaign.stats.discovered} / ${campaign.stats.target}`} />
          <Stat label="Researched" value={String(campaign.stats.researched)} />
          <Stat label="Failed" value={String(campaign.stats.failed)} />
          <Stat label="Qualified" value={String(campaign.stats.qualified)} />
          <Stat label="Approved" value={String(campaign.stats.approved)} />
          <Stat label="Total cost" value={`$${campaign.stats.total_research_cost.toFixed(4)}`} />
          <Stat
            label="Avg cost/company"
            value={`$${campaign.stats.average_cost_per_company.toFixed(4)}`}
          />
          <Stat label="Status" value={campaign.status} />
        </section>
        <section className="panel">
          <div className="panelHeader">
            <div>
              <h2>Ranked companies</h2>
              <p>Companies are deduped by normalized domain before research.</p>
            </div>
            <Link className="secondaryButton" href="/opportunities">
              Review approvals
            </Link>
          </div>
          <div className="campaignCompanyList">
            {campaign.companies.map((result) => (
              <CompanyResult key={result.entry.id} result={result} pending={pending} onRetry={retry} />
            ))}
            {!campaign.companies.length && <div className="empty">Run the campaign to discover companies.</div>}
          </div>
        </section>
      </section>
    </main>
  );
}

function CompanyResult({
  result,
  pending,
  onRetry,
}: {
  result: CampaignCompanyResult;
  pending: string | null;
  onRetry: (entryId: number) => void;
}) {
  return (
    <article className="campaignCompanyRow">
      <div>
        <strong>{result.entry.company.name}</strong>
        <small>{result.entry.company.domain}</small>
        {result.entry.error ? <p className="errorText">{result.entry.error}</p> : null}
      </div>
      <div className="scoreBreakdown inline">
        <Metric label="Total" value={result.score?.total_score ?? 0} />
        <Metric label="ICP" value={result.score?.icp_score ?? 0} />
        <Metric label="Pain" value={result.score?.pain_score ?? 0} />
        <Metric label="Value" value={result.score?.value_score ?? 0} />
      </div>
      <div className="signalsCell">
        {(result.score?.matched_signals ?? []).slice(0, 4).map((signal) => (
          <span key={signal}>{signal}</span>
        ))}
      </div>
      <div className="evidenceCell">
        {result.top_evidence.slice(0, 2).map((item) => (
          <p key={item.id}>{item.content_excerpt}</p>
        ))}
      </div>
      <div>
        <span className={`status ${result.entry.research_state === "FAILED" ? "failed" : "done"}`}>
          {result.entry.research_state}
        </span>
        {result.entry.research_state === "FAILED" ? (
          <button
            className="secondaryButton tiny"
            onClick={() => onRetry(result.entry.id)}
            disabled={pending === `retry-${result.entry.id}`}
          >
            Retry
          </button>
        ) : null}
      </div>
    </article>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="metric compactMetric">
      <span>{label}</span>
      <strong>{Math.round(value)}</strong>
    </div>
  );
}
