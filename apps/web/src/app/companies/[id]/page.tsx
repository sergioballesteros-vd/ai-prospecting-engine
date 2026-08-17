"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { CompanyTimeline, PipelineEvent, getCompanyTimeline } from "@/lib/api";
import { pipelineStateLabel } from "@/lib/labels";

export default function CompanyTimelinePage() {
  const params = useParams<{ id: string }>();
  const companyId = Number(params.id);
  const [company, setCompany] = useState<CompanyTimeline | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getCompanyTimeline(companyId)
      .then(setCompany)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "No se pudo cargar la cronología de la empresa"),
      );
  }, [companyId]);

  return (
    <AppShell>
      <section className="workspace">
        {error ? <div className="notice error">{error}</div> : null}
        {company ? (
          <>
            <header className="topbar">
              <div>
                <h1>{company.name}</h1>
                <p>
                  {company.domain} · {company.city ?? "Ciudad desconocida"} ·{" "}
                  {company.industry ?? "Industria desconocida"}
                </p>
              </div>
              <a className="secondaryButton" href={company.website_url} target="_blank" rel="noreferrer">
                Web
              </a>
            </header>
            <section className="panel timelinePanel">
              <div className="panelHeader">
                <div>
                  <h2>Cronología</h2>
                  <p>Eventos cronológicos de investigación, cualificación y actividad comercial.</p>
                </div>
              </div>
              <div className="timelineList">
                <TimelineItem label="Descubierta" timestamp={company.created_at} notes={company.website_url} />
                {company.evidence.length ? (
                  <TimelineItem
                    label="Investigada"
                    timestamp={company.evidence[0].detected_at}
                    notes={`${company.evidence.length} evidencias`}
                  />
                ) : null}
                {company.timeline.map((event) => (
                  <PipelineTimelineItem event={event} key={event.id} />
                ))}
                {!company.timeline.length && !company.evidence.length ? (
                  <div className="empty">Todavía no hay eventos comerciales.</div>
                ) : null}
              </div>
            </section>
          </>
        ) : (
          <div className="empty">Cargando empresa...</div>
        )}
      </section>
    </AppShell>
  );
}

function PipelineTimelineItem({ event }: { event: PipelineEvent }) {
  const details = [
    event.channel ? `Canal: ${event.channel}` : null,
    event.lost_reason ? `Pérdida: ${event.lost_reason}` : null,
    event.expected_revenue ? `Ingresos: ${event.currency ?? "EUR"} ${event.expected_revenue}` : null,
    event.recurring_revenue_monthly ? `MRR: ${event.currency ?? "EUR"} ${event.recurring_revenue_monthly}` : null,
    event.notes,
  ].filter(Boolean);
  return (
    <TimelineItem
      label={pipelineStateLabel(event.to_state)}
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
