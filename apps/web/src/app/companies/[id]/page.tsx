"use client";

import { BarChart3, FileSearch, Search, Send, Sparkles } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { CompanyTimeline, PipelineEvent, getCompanyTimeline } from "@/lib/api";

export default function CompanyTimelinePage() {
  const params = useParams<{ id: string }>();
  const companyId = Number(params.id);
  const [company, setCompany] = useState<CompanyTimeline | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getCompanyTimeline(companyId)
      .then(setCompany)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Could not load company timeline"),
      );
  }, [companyId]);

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
          <Link className="navItem" href="/campaigns">
            <Send size={17} />
            Campaigns
          </Link>
          <Link className="navItem" href="/opportunities">
            <Sparkles size={17} />
            Opportunities
          </Link>
          <Link className="navItem" href="/analytics">
            <BarChart3 size={17} />
            Analytics
          </Link>
        </nav>
      </aside>
      <section className="workspace">
        {error ? <div className="notice error">{error}</div> : null}
        {company ? (
          <>
            <header className="topbar">
              <div>
                <h1>{company.name}</h1>
                <p>
                  {company.domain} · {company.city ?? "Unknown city"} ·{" "}
                  {company.industry ?? "Unknown industry"}
                </p>
              </div>
              <a className="secondaryButton" href={company.website_url} target="_blank" rel="noreferrer">
                Website
              </a>
            </header>
            <section className="panel timelinePanel">
              <div className="panelHeader">
                <div>
                  <h2>Timeline</h2>
                  <p>Chronological research, qualification and commercial events.</p>
                </div>
              </div>
              <div className="timelineList">
                <TimelineItem label="DISCOVERED" timestamp={company.created_at} notes={company.website_url} />
                {company.evidence.length ? (
                  <TimelineItem
                    label="RESEARCHED"
                    timestamp={company.evidence[0].detected_at}
                    notes={`${company.evidence.length} evidence items`}
                  />
                ) : null}
                {company.timeline.map((event) => (
                  <PipelineTimelineItem event={event} key={event.id} />
                ))}
                {!company.timeline.length && !company.evidence.length ? (
                  <div className="empty">No commercial events yet.</div>
                ) : null}
              </div>
            </section>
          </>
        ) : (
          <div className="empty">Loading company...</div>
        )}
      </section>
    </main>
  );
}

function PipelineTimelineItem({ event }: { event: PipelineEvent }) {
  const details = [
    event.channel ? `Channel: ${event.channel}` : null,
    event.lost_reason ? `Lost: ${event.lost_reason}` : null,
    event.expected_revenue ? `Revenue: ${event.currency ?? "EUR"} ${event.expected_revenue}` : null,
    event.recurring_revenue_monthly ? `MRR: ${event.currency ?? "EUR"} ${event.recurring_revenue_monthly}` : null,
    event.notes,
  ].filter(Boolean);
  return (
    <TimelineItem
      label={event.to_state}
      timestamp={event.timestamp}
      notes={details.join(" · ")}
    />
  );
}

function TimelineItem({
  label,
  timestamp,
  notes,
}: {
  label: string;
  timestamp: string;
  notes: string;
}) {
  return (
    <article className="timelineItem">
      <span className="status done">{label}</span>
      <div>
        <strong>{new Date(timestamp).toLocaleString()}</strong>
        <p>{notes}</p>
      </div>
    </article>
  );
}
