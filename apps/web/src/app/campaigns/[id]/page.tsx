"use client";

import { BarChart3, FileSearch, RefreshCw, Search, Send, Sparkles } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import {
  CampaignCompanyResult,
  FunnelAnalytics,
  ProspectingCampaignDetail,
  getCampaignAnalytics,
  getCampaign,
  retryCampaignCompany,
  runCampaign,
} from "@/lib/api";
import { campaignStatusLabel, pipelineStateLabel, researchStateLabel, signalLabel } from "@/lib/labels";

export default function CampaignDetailPage() {
  const params = useParams<{ id: string }>();
  const campaignId = Number(params.id);
  const [campaign, setCampaign] = useState<ProspectingCampaignDetail | null>(null);
  const [analytics, setAnalytics] = useState<FunnelAnalytics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const [nextCampaign, nextAnalytics] = await Promise.all([
        getCampaign(campaignId),
        getCampaignAnalytics(campaignId),
      ]);
      setCampaign(nextCampaign);
      setAnalytics(nextAnalytics);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo cargar la campaña");
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
      setError(err instanceof Error ? err.message : "No se pudo ejecutar la campaña");
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
      setError(err instanceof Error ? err.message : "No se pudo reintentar");
    } finally {
      setPending(null);
    }
  }

  if (!campaign) {
    return <div className="empty">Cargando campaña...</div>;
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
            Investigación
          </Link>
          <Link className="navItem active" href="/campaigns">
            <Send size={17} />
            Campañas
          </Link>
          <Link className="navItem" href="/opportunities">
            <Sparkles size={17} />
            Oportunidades
          </Link>
          <Link className="navItem" href="/analytics">
            <BarChart3 size={17} />
            Analítica
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
            {campaign.status === "DRAFT" ? "Ejecutar campaña" : "Ejecutar de nuevo"}
          </button>
        </header>
        {error ? <div className="notice error">{error}</div> : null}
        <section className="campaignStats">
          <Stat label="Descubiertas" value={`${campaign.stats.discovered} / ${campaign.stats.target}`} />
          <Stat label="Investigadas" value={String(campaign.stats.researched)} />
          <Stat label="Fallidas" value={String(campaign.stats.failed)} />
          <Stat label="Cualificadas" value={String(campaign.stats.qualified)} />
          <Stat label="Aprobadas" value={String(campaign.stats.approved)} />
          <Stat label="Coste total" value={`$${campaign.stats.total_research_cost.toFixed(4)}`} />
          <Stat
            label="Coste medio/empresa"
            value={`$${campaign.stats.average_cost_per_company.toFixed(4)}`}
          />
          <Stat label="Estado" value={campaignStatusLabel(campaign.status)} />
        </section>
        {analytics ? (
          <section className="campaignStats">
            <Stat label="Contactadas" value={String(analytics.counts.contacted)} />
            <Stat label="Respondieron" value={String(analytics.counts.replied)} />
            <Stat label="Reuniones" value={String(analytics.counts.meetings)} />
            <Stat label="Propuestas" value={String(analytics.counts.proposals)} />
            <Stat label="Ganadas" value={String(analytics.counts.won)} />
            <Stat label="Perdidas" value={String(analytics.counts.lost)} />
            <Stat
              label="Ingresos"
              value={`€${analytics.business_metrics.revenue_generated.toFixed(0)}`}
            />
            <Stat label="MRR" value={`€${analytics.business_metrics.mrr_generated.toFixed(0)}`} />
          </section>
        ) : null}
        <section className="panel">
          <div className="panelHeader">
            <div>
              <h2>Empresas priorizadas</h2>
              <p>Las empresas se deduplican por dominio normalizado antes de investigarlas.</p>
            </div>
            <Link className="secondaryButton" href="/opportunities">
              Revisar aprobaciones
            </Link>
          </div>
          <div className="campaignCompanyList">
            {campaign.companies.map((result) => (
              <CompanyResult key={result.entry.id} result={result} pending={pending} onRetry={retry} />
            ))}
            {!campaign.companies.length && <div className="empty">Ejecuta la campaña para descubrir empresas.</div>}
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
        <Link className="secondaryButton tiny" href={`/companies/${result.entry.company.id}`}>
          Cronología
        </Link>
        {result.entry.error ? <p className="errorText">{result.entry.error}</p> : null}
      </div>
      <div className="scoreBreakdown inline">
        <Metric label="Total" value={result.score?.total_score ?? 0} />
        <Metric label="ICP" value={result.score?.icp_score ?? 0} />
        <Metric label="Dolor" value={result.score?.pain_score ?? 0} />
        <Metric label="Valor" value={result.score?.value_score ?? 0} />
      </div>
      <div className="signalsCell">
        {(result.score?.matched_signals ?? []).slice(0, 4).map((signal) => (
          <span key={signal}>{signalLabel(signal)}</span>
        ))}
      </div>
      <div className="evidenceCell">
        {result.top_evidence.slice(0, 2).map((item) => (
          <p key={item.id}>{item.content_excerpt}</p>
        ))}
      </div>
      <div>
        <span className={`status ${result.entry.research_state === "FAILED" ? "failed" : "done"}`}>
          {researchStateLabel(result.entry.research_state)}
        </span>
        {result.pipeline_state ? (
          <span className={`status ${result.pipeline_state === "LOST" ? "failed" : "done"}`}>
            {pipelineStateLabel(result.pipeline_state)}
          </span>
        ) : null}
        {result.entry.research_state === "FAILED" ? (
          <button
            className="secondaryButton tiny"
            onClick={() => onRetry(result.entry.id)}
            disabled={pending === `retry-${result.entry.id}`}
          >
            Reintentar
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
