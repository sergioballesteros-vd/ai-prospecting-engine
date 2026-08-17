"use client";

import { Plus } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { ProspectingCampaign, listCampaigns } from "@/lib/api";
import { campaignStatusLabel } from "@/lib/labels";

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<ProspectingCampaign[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listCampaigns()
      .then(setCampaigns)
      .catch((err) => setError(err instanceof Error ? err.message : "No se pudieron cargar las campañas"));
  }, []);

  return (
    <AppShell>
      <section className="workspace">
        <header className="topbar">
          <div>
            <h1>Campañas</h1>
            <p>Define un mercado objetivo, descubre empresas, investígalas y prioriza resultados.</p>
          </div>
          <Link className="secondaryButton" href="/campaigns/new">
            <Plus size={16} />
            Nueva campaña
          </Link>
        </header>
        {error ? <div className="notice error">{error}</div> : null}
        <section className="panel">
          <div className="panelHeader">
            <div>
              <h2>Campañas de prospección</h2>
              <p>Las campañas no envían outreach automáticamente.</p>
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
                <span>{campaign.target_company_count} objetivos</span>
                <span className={`status ${campaign.status === "COMPLETED" ? "done" : "live"}`}>
                  {campaignStatusLabel(campaign.status)}
                </span>
              </Link>
            ))}
            {!campaigns.length && <div className="empty">Crea una campaña para empezar el descubrimiento.</div>}
          </div>
        </section>
      </section>
    </AppShell>
  );
}
