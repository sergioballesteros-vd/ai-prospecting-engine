"use client";

import { FileSearch, Plus, Search, Send, Sparkles } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { ProspectingCampaign, listCampaigns } from "@/lib/api";

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<ProspectingCampaign[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listCampaigns()
      .then(setCampaigns)
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load campaigns"));
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
            <h1>Campaigns</h1>
            <p>Define a target market, discover companies, research them, and rank results.</p>
          </div>
          <Link className="secondaryButton" href="/campaigns/new">
            <Plus size={16} />
            New campaign
          </Link>
        </header>
        {error ? <div className="notice error">{error}</div> : null}
        <section className="panel">
          <div className="panelHeader">
            <div>
              <h2>Prospecting campaigns</h2>
              <p>No outreach is sent from campaigns.</p>
            </div>
            <span>{campaigns.length}</span>
          </div>
          <div className="rankedList">
            {campaigns.map((campaign) => (
              <Link className="campaignRow" href={`/campaigns/${campaign.id}`} key={campaign.id}>
                <span>
                  <strong>{campaign.name}</strong>
                  <small>
                    {campaign.city_or_region}, {campaign.country} · {campaign.industries.join(", ")}
                  </small>
                </span>
                <span>{campaign.target_company_count} targets</span>
                <span className={`status ${campaign.status === "COMPLETED" ? "done" : "live"}`}>
                  {campaign.status}
                </span>
              </Link>
            ))}
            {!campaigns.length && <div className="empty">Create a campaign to start discovery.</div>}
          </div>
        </section>
      </section>
    </main>
  );
}
