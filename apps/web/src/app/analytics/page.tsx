"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
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
        setError(err instanceof Error ? err.message : "No se pudo cargar la analítica"),
      );
  }, []);

  return (
    <AppShell>
      <section className="workspace">
        <header className="topbar">
          <div>
            <h1>Analítica comercial</h1>
            <p>Resultados manuales del funnel, comparación de campañas y atribución de ingresos.</p>
          </div>
        </header>
        {error ? <div className="notice error">{error}</div> : null}
        {funnel ? (
          <>
            <section className="campaignStats">
              <Stat label="Descubiertas" value={funnel.counts.discovered} />
              <Stat label="Investigadas" value={funnel.counts.researched} />
              <Stat label="Cualificadas" value={funnel.counts.qualified} />
              <Stat label="Aprobadas" value={funnel.counts.approved} />
              <Stat label="Contactadas" value={funnel.counts.contacted} />
              <Stat label="Respondieron" value={funnel.counts.replied} />
              <Stat label="Reuniones" value={funnel.counts.meetings} />
              <Stat label="Propuestas" value={funnel.counts.proposals} />
              <Stat label="Ganadas" value={funnel.counts.won} />
              <Stat label="Perdidas" value={funnel.counts.lost} />
            </section>
            <section className="campaignStats">
              <Stat
                label="Contactado -> Respuesta"
                value={`${percent(funnel.conversion_rates.contacted_to_reply)}%`}
              />
              <Stat
                label="Respuesta -> Reunión"
                value={`${percent(funnel.conversion_rates.reply_to_meeting)}%`}
              />
              <Stat
                label="Reunión -> Propuesta"
                value={`${percent(funnel.conversion_rates.meeting_to_proposal)}%`}
              />
              <Stat
                label="Propuesta -> Ganado"
                value={`${percent(funnel.conversion_rates.proposal_to_won)}%`}
              />
            </section>
            <section className="campaignStats">
              <Stat
                label="Ingresos generados"
                value={`€${funnel.business_metrics.revenue_generated.toFixed(0)}`}
              />
              <Stat label="MRR generado" value={`€${funnel.business_metrics.mrr_generated.toFixed(0)}`} />
              <Stat
                label="Ticket medio"
                value={`€${funnel.business_metrics.average_deal_value.toFixed(0)}`}
              />
              <Stat
                label="Ingresos / 100 descubiertas"
                value={`€${funnel.business_metrics.revenue_per_100_discovered.toFixed(0)}`}
              />
              <Stat
                label="Ingresos / 100 contactadas"
                value={`€${funnel.business_metrics.revenue_per_100_contacted.toFixed(0)}`}
              />
              <Stat
                label="Coste / reunión"
                value={`€${funnel.business_metrics.research_cost_per_meeting.toFixed(4)}`}
              />
              <Stat
                label="Coste / cliente ganado"
                value={`€${funnel.business_metrics.research_cost_per_won_customer.toFixed(4)}`}
              />
            </section>
          </>
        ) : (
          <div className="empty">Cargando analítica...</div>
        )}
        <section className="panel analyticsPanel">
          <div className="panelHeader">
            <div>
              <h2>Comparación de campañas</h2>
              <p>Compara sectores por volumen descubierto, conversión, ingresos y coste de investigación.</p>
            </div>
          </div>
          <div className="comparisonTable">
            <div className="comparisonHeader">
              <span>Campaña</span>
              <span>Sector</span>
              <span>Descubiertas</span>
              <span>Cualificadas</span>
              <span>Respuesta</span>
              <span>Reunión</span>
              <span>Ganadas</span>
              <span>Ingresos</span>
              <span>MRR</span>
              <span>Coste</span>
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
            {!campaigns.length ? <div className="empty">Todavía no hay campañas.</div> : null}
          </div>
        </section>
      </section>
    </AppShell>
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
