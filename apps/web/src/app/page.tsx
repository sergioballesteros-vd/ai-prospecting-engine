"use client";

import {
  AlertCircle,
  CheckCircle2,
  Loader2,
  Play,
} from "lucide-react";
import { FormEvent, useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
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
import { jobStatusLabel, signalLabel } from "@/lib/labels";

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
        setError(err instanceof Error ? err.message : "No se pudo actualizar el estado del trabajo");
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
      setError(err instanceof Error ? err.message : "No se pudo iniciar la investigación");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AppShell>
      <section className="workspace">
        <header className="topbar">
          <div>
            <h1>Investigación</h1>
            <p>Introduce un dominio, extrae evidencia pública y revisa el análisis estructurado.</p>
          </div>
          <span className="environment">Sin envío automático</span>
        </header>

        <form className="researchForm" onSubmit={submit}>
          <label>
            <span>Dominio de la empresa</span>
            <input
              value={domain}
              onChange={(event) => setDomain(event.target.value)}
              placeholder="example.com"
              required
            />
          </label>
          <button type="submit" disabled={isSubmitting || !domain.trim()}>
            {isSubmitting ? <Loader2 className="spin" size={16} /> : <Play size={16} />}
            Investigar
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
    </AppShell>
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
        <span className="label">Empresa</span>
        <strong>{company ? company.name : "Sin seleccionar"}</strong>
      </div>
      <div>
        <span className="label">Último trabajo</span>
        <strong className={`status ${statusClass}`}>{jobStatusLabel(job ? job.status : "idle")}</strong>
      </div>
      <div>
        <span className="label">Fuentes</span>
        <strong>{detail?.sources.length ?? 0}</strong>
      </div>
      <div>
        <span className="label">Evidencia</span>
        <strong>{detail?.evidence.length ?? 0}</strong>
      </div>
      <div className="statusMessage">
        <span className="label">Mensaje</span>
        <strong>{job?.error || translateJobMessage(job?.message) || "Esperando investigación"}</strong>
      </div>
    </section>
  );
}

function EvidencePanel({ detail }: { detail: CompanyDetail | null }) {
  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>Evidencia</h2>
          <p>Las señales son trazables a URLs públicas.</p>
        </div>
        <span>{detail?.evidence.length ?? 0}</span>
      </div>
      <div className="evidenceList">
        {detail?.evidence.length ? (
          detail.evidence.map((item) => (
            <article className="evidenceRow" key={item.id}>
              <div>
                <div className="rowTitle">
                  <span>{signalLabel(item.signal_type)}</span>
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
          <EmptyState text="Lanza una investigación para recopilar evidencia." />
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
          <h2>Análisis IA</h2>
          <p>Salida estructurada, limitada a la evidencia recopilada.</p>
        </div>
        {job?.status === "running" ? <Loader2 className="spin" size={18} /> : null}
      </div>
      {analysis ? (
        <div className="analysis">
          <section>
            <h3>Resumen</h3>
            <p>{analysis.summary}</p>
          </section>
          <section>
            <h3>Señales observadas</h3>
            <ul>
              {analysis.observed_signals.map((signal) => (
                <li key={`${signal.signalType}-${signal.evidenceIds.join("-")}`}>
                  <CheckCircle2 size={15} />
                  <span>
                    <strong>{signalLabel(signal.signalType)}</strong> {signal.reasoning}
                    <small>Evidencia #{signal.evidenceIds.join(", #")}</small>
                  </span>
                </li>
              ))}
            </ul>
          </section>
          <section>
            <h3>Posibles oportunidades de automatización</h3>
            {analysis.possible_automation_opportunities.map((opportunity) => (
              <div className="opportunity" key={opportunity.problem}>
                <strong>{opportunity.problem}</strong>
                <p>{opportunity.reasoning}</p>
                <small>Evidencia #{opportunity.evidenceIds.join(", #")}</small>
              </div>
            ))}
          </section>
          <section className="columns">
            <div>
              <h3>Desconocidos</h3>
              {analysis.unknowns.map((unknown) => (
                <p key={unknown}>? {unknown}</p>
              ))}
            </div>
            <div>
              <h3>Roles compradores</h3>
              {analysis.recommended_buyer_roles.map((role) => (
                <p key={role}>{role}</p>
              ))}
            </div>
          </section>
        </div>
      ) : (
        <EmptyState text="El análisis estructurado aparecerá tras extraer evidencia." />
      )}
    </section>
  );
}

function EmptyState({ text }: { text: string }) {
  return <div className="empty">{text}</div>;
}

function translateJobMessage(message: string | null | undefined) {
  if (!message) return null;
  const labels: Record<string, string> = {
    "Research queued": "Investigación en cola",
    "Fetching website pages": "Recopilando páginas web",
    "Research completed": "Investigación completada",
    "Research failed": "La investigación falló",
  };
  return labels[message] ?? message;
}
