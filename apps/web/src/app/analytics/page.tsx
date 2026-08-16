"use client";

import { BarChart3, FileSearch, Search, Send, Sparkles } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import {
  CampaignComparison,
  FunnelAnalytics,
  getCampaignComparison,
  getGlobalFunnel,
} from "@/lib/api";

export default function AnalyticsPage() {
  const [funnel, setFunnel] = useState<FunnelAnalytics | null>(null);
  const [campaigns, setCampaigns] = useState<CampaignComparison[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getGlobalFunnel(), getCampaignComparison()])
      .then(([nextFunnel, nextCampaigns]) => {
        setFunnel(nextFunnel);
        setCampaigns(nextCampaigns);
      })
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Could not load analytics"),
      );
  }, []);

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
          <Link className="navItem active" href="/analytics">
            <BarChart3 size={17} />
            Analytics
          </Link>
        </nav>
      </aside>
      <section className="workspace">
        <header className="topbar">
          <div>
            <h1>Commercial analytics</h1>
            <p>Manual funnel outcomes, campaign comparison and revenue attribution.</p>
          </div>
        </header>
        {error ? <div className="notice error">{error}</div> : null}
        {funnel ? (
          <>
            <section className="campaignStats">
              <Stat label="Discovered" value={funnel.counts.discovered} />
              <Stat label="Researched" value={funnel.counts.researched} />
              <Stat label="Qualified" value={funnel.counts.qualified} />
              <Stat label="Approved" value={funnel.counts.approved} />
              <Stat label="Contacted" value={funnel.counts.contacted} />
              <Stat label="Replied" value={funnel.counts.replied} />
              <Stat label="Meetings" value={funnel.counts.meetings} />
              <Stat label="Proposals" value={funnel.counts.proposals} />
              <Stat label="Won" value={funnel.counts.won} />
              <Stat label="Lost" value={funnel.counts.lost} />
            </section>
            <section className="campaignStats">
              <Stat
                label="Contacted -> Reply"
                value={`${percent(funnel.conversion_rates.contacted_to_reply)}%`}
              />
              <Stat
                label="Reply -> Meeting"
                value={`${percent(funnel.conversion_rates.reply_to_meeting)}%`}
              />
              <Stat
                label="Meeting -> Proposal"
                value={`${percent(funnel.conversion_rates.meeting_to_proposal)}%`}
              />
              <Stat
                label="Proposal -> Won"
                value={`${percent(funnel.conversion_rates.proposal_to_won)}%`}
              />
            </section>
            <section className="campaignStats">
              <Stat
                label="Revenue generated"
                value={`€${funnel.business_metrics.revenue_generated.toFixed(0)}`}
              />
              <Stat label="MRR generated" value={`€${funnel.business_metrics.mrr_generated.toFixed(0)}`} />
              <Stat
                label="Average deal"
                value={`€${funnel.business_metrics.average_deal_value.toFixed(0)}`}
              />
              <Stat
                label="Revenue / 100 discovered"
                value={`€${funnel.business_metrics.revenue_per_100_discovered.toFixed(0)}`}
              />
              <Stat
                label="Revenue / 100 contacted"
                value={`€${funnel.business_metrics.revenue_per_100_contacted.toFixed(0)}`}
              />
              <Stat
                label="Cost / meeting"
                value={`€${funnel.business_metrics.research_cost_per_meeting.toFixed(4)}`}
              />
              <Stat
                label="Cost / won customer"
                value={`€${funnel.business_metrics.research_cost_per_won_customer.toFixed(4)}`}
              />
            </section>
          </>
        ) : (
          <div className="empty">Loading analytics...</div>
        )}
        <section className="panel analyticsPanel">
          <div className="panelHeader">
            <div>
              <h2>Campaign comparison</h2>
              <p>Compare sectors by discovery volume, conversion, revenue and research cost.</p>
            </div>
          </div>
          <div className="comparisonTable">
            <div className="comparisonHeader">
              <span>Campaign</span>
              <span>Sector</span>
              <span>Discovered</span>
              <span>Qualified</span>
              <span>Reply</span>
              <span>Meeting</span>
              <span>Win</span>
              <span>Revenue</span>
              <span>MRR</span>
              <span>Cost</span>
            </div>
            {campaigns.map((campaign) => (
              <Link
                className="comparisonRow"
                href={`/campaigns/${campaign.campaign_id}`}
                key={campaign.campaign_id}
              >
                <strong>{campaign.name}</strong>
                <span>{campaign.sector}</span>
                <span>{campaign.companies_discovered}</span>
                <span>{campaign.qualified}</span>
                <span>{percent(campaign.reply_rate)}%</span>
                <span>{percent(campaign.meeting_rate)}%</span>
                <span>{percent(campaign.win_rate)}%</span>
                <span>€{campaign.revenue.toFixed(0)}</span>
                <span>€{campaign.mrr.toFixed(0)}</span>
                <span>€{campaign.research_cost.toFixed(4)}</span>
              </Link>
            ))}
            {!campaigns.length ? <div className="empty">No campaigns yet.</div> : null}
          </div>
        </section>
      </section>
    </main>
  );
}

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function percent(value: number) {
  return Math.round(value * 100);
}
