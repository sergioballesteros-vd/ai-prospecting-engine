"use client";

import {
  Check,
  Loader2,
  MailPlus,
  Save,
  X,
} from "lucide-react";
import Link from "next/link";
import type { Dispatch, SetStateAction } from "react";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  OutreachDraft,
  PipelineState,
  RankedOpportunity,
  createPipelineEvent,
  generateDraft,
  listRankedOpportunities,
  updateDraft,
  updateOpportunityState,
} from "@/lib/api";
import { pipelineStateLabel, reviewStateLabel, signalLabel } from "@/lib/labels";

export default function OpportunitiesPage() {
  const [rows, setRows] = useState<RankedOpportunity[]>([]);
  const [selected, setSelected] = useState<RankedOpportunity | null>(null);
  const [draftEdits, setDraftEdits] = useState<Record<number, { subject: string; body: string }>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [pendingAction, setPendingAction] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    refresh();
  }, []);

  async function refresh() {
    setError(null);
    setIsLoading(true);
    try {
      const nextRows = await listRankedOpportunities();
      setRows(nextRows);
      setSelected((current) => {
        if (!current) return nextRows[0] ?? null;
        return nextRows.find((row) => row.score.id === current.score.id) ?? nextRows[0] ?? null;
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudieron cargar las oportunidades");
    } finally {
      setIsLoading(false);
    }
  }

  async function review(row: RankedOpportunity, state: "APPROVED" | "REJECTED") {
    setPendingAction(`${state}-${row.score.id}`);
    setError(null);
    try {
      const updated = await updateOpportunityState(row.score.id, state);
      replaceRow(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo guardar la revisión");
    } finally {
      setPendingAction(null);
    }
  }

  async function createDraft(row: RankedOpportunity) {
    setPendingAction(`DRAFT-${row.score.id}`);
    setError(null);
    try {
      const draft = await generateDraft(row.score.id);
      const updated = { ...row, latest_draft: draft };
      replaceRow(updated);
      setDraftEdits((current) => ({
        ...current,
        [draft.id]: { subject: draft.subject, body: draft.body },
      }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo generar el borrador");
    } finally {
      setPendingAction(null);
    }
  }

  async function saveDraft(draft: OutreachDraft) {
    const edits = draftEdits[draft.id];
    if (!edits) return;
    setPendingAction(`SAVE-${draft.id}`);
    setError(null);
    try {
      const updatedDraft = await updateDraft(draft.id, { ...edits, status: draft.status });
      if (!selected) return;
      replaceRow({ ...selected, latest_draft: updatedDraft });
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo guardar el borrador");
    } finally {
      setPendingAction(null);
    }
  }

  async function movePipeline(
    row: RankedOpportunity,
    payload: {
      to_state: PipelineState;
      notes?: string | null;
      channel?: "EMAIL" | "LINKEDIN" | "PHONE" | "OTHER" | null;
      message_used?: string | null;
      expected_revenue?: number | null;
      recurring_revenue_monthly?: number | null;
      implementation_revenue?: number | null;
      currency?: string | null;
      lost_reason?: string | null;
    },
  ) {
    setPendingAction(`PIPELINE-${row.score.id}`);
    setError(null);
    try {
      const event = await createPipelineEvent({
        company_id: row.company.id,
        opportunity_id: row.score.opportunity_id,
        ...payload,
      });
      replaceRow({ ...row, pipeline_state: event.to_state });
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo mover el pipeline");
    } finally {
      setPendingAction(null);
    }
  }

  function replaceRow(updated: RankedOpportunity) {
    setRows((current) =>
      current.map((row) => (row.score.id === updated.score.id ? updated : row)),
    );
    setSelected(updated);
  }

  return (
    <AppShell>
      <section className="workspace">
        <header className="topbar">
          <div>
            <h1>Oportunidades priorizadas</h1>
            <p>Revisa scores determinísticos, inspecciona evidencia y aprueba o rechaza.</p>
          </div>
          <button className="secondaryButton" onClick={refresh} disabled={isLoading}>
            {isLoading ? <Loader2 className="spin" size={16} /> : null}
            Actualizar scores
          </button>
        </header>

        {error ? <div className="notice error">{error}</div> : null}

        <section className="reviewGrid">
          <div className="panel">
            <div className="panelHeader">
              <div>
                <h2>Empresas</h2>
                <p>El score total usa pesos configurables por oportunidad.</p>
              </div>
              <span>{rows.length}</span>
            </div>
            <div className="rankedList">
              {rows.map((row) => (
                <button
                  className={`rankedRow ${
                    selected?.score.id === row.score.id ? "selected" : ""
                  }`}
                  key={row.score.id}
                  onClick={() => setSelected(row)}
                >
                  <span className="scoreBadge">{Math.round(row.score.total_score)}</span>
                  <span>
                    <strong>{row.company.name}</strong>
                    <small>{row.company.domain}</small>
                  </span>
                  <span className={`status ${stateClass(row.score.qualification_state)}`}>
                    {reviewStateLabel(row.score.qualification_state)}
                  </span>
                </button>
              ))}
              {!rows.length && <div className="empty">Investiga alguna empresa antes de revisar oportunidades.</div>}
            </div>
          </div>

          <OpportunityDetail
            row={selected}
            pendingAction={pendingAction}
            draftEdits={draftEdits}
            setDraftEdits={setDraftEdits}
            onReview={review}
            onCreateDraft={createDraft}
            onSaveDraft={saveDraft}
            onMovePipeline={movePipeline}
          />
        </section>
      </section>
    </AppShell>
  );
}

function OpportunityDetail({
  row,
  pendingAction,
  draftEdits,
  setDraftEdits,
  onReview,
  onCreateDraft,
  onSaveDraft,
  onMovePipeline,
}: {
  row: RankedOpportunity | null;
  pendingAction: string | null;
  draftEdits: Record<number, { subject: string; body: string }>;
  setDraftEdits: Dispatch<SetStateAction<Record<number, { subject: string; body: string }>>>;
  onReview: (row: RankedOpportunity, state: "APPROVED" | "REJECTED") => void;
  onCreateDraft: (row: RankedOpportunity) => void;
  onSaveDraft: (draft: OutreachDraft) => void;
  onMovePipeline: (
    row: RankedOpportunity,
    payload: {
      to_state: PipelineState;
      notes?: string | null;
      channel?: "EMAIL" | "LINKEDIN" | "PHONE" | "OTHER" | null;
      message_used?: string | null;
      expected_revenue?: number | null;
      recurring_revenue_monthly?: number | null;
      implementation_revenue?: number | null;
      currency?: string | null;
      lost_reason?: string | null;
    },
  ) => void;
}) {
  const [pipelineForm, setPipelineForm] = useState({
    notes: "",
    channel: "EMAIL" as "EMAIL" | "LINKEDIN" | "PHONE" | "OTHER",
    message_used: "",
    expected_revenue: "",
    recurring_revenue_monthly: "",
    implementation_revenue: "",
    currency: "EUR",
    lost_reason: "",
  });

  if (!row) {
    return (
      <div className="panel">
        <div className="empty">Selecciona una empresa priorizada.</div>
      </div>
    );
  }

  const draft = row.latest_draft;
  const edits = draft
    ? (draftEdits[draft.id] ?? { subject: draft.subject, body: draft.body })
    : null;
  const nextState = nextPipelineState(row.pipeline_state);
  const canManagePipeline =
    row.score.qualification_state === "APPROVED" && row.pipeline_state !== "WON" && row.pipeline_state !== "LOST";

  return (
    <div className="panel detailPanel">
      <div className="panelHeader">
        <div>
          <h2>{row.company.name}</h2>
          <p>{row.why_matched}</p>
        </div>
        <span className="scoreBadge large">{Math.round(row.score.total_score)}</span>
      </div>

      <section className="scoreBreakdown">
        <Metric label="ICP" value={row.score.icp_score} />
        <Metric label="Dolor" value={row.score.pain_score} />
        <Metric label="Valor" value={row.score.value_score} />
        <Metric label="Intención" value={row.score.intent_score} />
        <Metric label="Alcance" value={row.score.reachability_score} />
        <Metric label="Confianza" value={row.score.confidence_score} />
      </section>

      <section className="detailSection">
        <h3>Evidencia principal</h3>
        {row.top_evidence.map((item) => (
          <article className="evidenceRow compact" key={item.id}>
            <div className="rowTitle">
              <span>
                #{item.id} {signalLabel(item.signal_type)}
              </span>
              <small>{Math.round(item.confidence * 100)}%</small>
            </div>
            <p>{item.content_excerpt}</p>
            <a href={item.source_url} target="_blank" rel="noreferrer">
              {item.source_url}
            </a>
          </article>
        ))}
      </section>

      <section className="reviewActions">
        <button
          className="dangerButton"
          onClick={() => onReview(row, "REJECTED")}
          disabled={pendingAction === `REJECTED-${row.score.id}`}
        >
          <X size={16} />
          Rechazar
        </button>
        <button
          onClick={() => onReview(row, "APPROVED")}
          disabled={pendingAction === `APPROVED-${row.score.id}`}
        >
          <Check size={16} />
          Aprobar
        </button>
        <button
          className="secondaryButton"
          onClick={() => onCreateDraft(row)}
          disabled={
            row.score.qualification_state !== "APPROVED" ||
            pendingAction === `DRAFT-${row.score.id}`
          }
        >
          <MailPlus size={16} />
          Generar borrador
        </button>
      </section>

      <section className="detailSection">
        <h3>Pipeline comercial</h3>
        <div className="pipelineHeader">
          <span className={`status ${row.pipeline_state ? stateClass(row.pipeline_state) : ""}`}>
            {pipelineStateLabel(row.pipeline_state)}
          </span>
          <Link className="secondaryButton tiny" href={`/companies/${row.company.id}`}>
            Cronología
          </Link>
        </div>
        {canManagePipeline && nextState ? (
          <div className="pipelineForm">
            {nextState === "CONTACTED" ? (
              <>
                <label>
                  <span>Canal</span>
                  <select
                    value={pipelineForm.channel}
                    onChange={(event) =>
                      setPipelineForm((current) => ({
                        ...current,
                        channel: event.target.value as typeof pipelineForm.channel,
                      }))
                    }
                  >
                    <option value="EMAIL">Email</option>
                    <option value="LINKEDIN">LinkedIn</option>
                    <option value="PHONE">Teléfono</option>
                    <option value="OTHER">Otro</option>
                  </select>
                </label>
                <label>
                  <span>Mensaje usado</span>
                  <textarea
                    value={pipelineForm.message_used}
                    onChange={(event) =>
                      setPipelineForm((current) => ({
                        ...current,
                        message_used: event.target.value,
                      }))
                    }
                  />
                </label>
              </>
            ) : null}
            {nextState === "WON" ? (
              <div className="revenueGrid">
                <label>
                  <span>Ingresos esperados</span>
                  <input
                    inputMode="decimal"
                    value={pipelineForm.expected_revenue}
                    onChange={(event) =>
                      setPipelineForm((current) => ({
                        ...current,
                        expected_revenue: event.target.value,
                      }))
                    }
                  />
                </label>
                <label>
                  <span>MRR</span>
                  <input
                    inputMode="decimal"
                    value={pipelineForm.recurring_revenue_monthly}
                    onChange={(event) =>
                      setPipelineForm((current) => ({
                        ...current,
                        recurring_revenue_monthly: event.target.value,
                      }))
                    }
                  />
                </label>
                <label>
                  <span>Implementación</span>
                  <input
                    inputMode="decimal"
                    value={pipelineForm.implementation_revenue}
                    onChange={(event) =>
                      setPipelineForm((current) => ({
                        ...current,
                        implementation_revenue: event.target.value,
                      }))
                    }
                  />
                </label>
                <label>
                  <span>Moneda</span>
                  <input
                    value={pipelineForm.currency}
                    onChange={(event) =>
                      setPipelineForm((current) => ({
                        ...current,
                        currency: event.target.value.toUpperCase().slice(0, 3),
                      }))
                    }
                  />
                </label>
              </div>
            ) : null}
            <label>
              <span>Notas</span>
              <textarea
                value={pipelineForm.notes}
                onChange={(event) =>
                  setPipelineForm((current) => ({ ...current, notes: event.target.value }))
                }
              />
            </label>
            {row.pipeline_state ? (
              <label>
                <span>Motivo de pérdida</span>
                <input
                  value={pipelineForm.lost_reason}
                  onChange={(event) =>
                    setPipelineForm((current) => ({
                      ...current,
                      lost_reason: event.target.value,
                    }))
                  }
                />
              </label>
            ) : null}
            <div className="reviewActions">
              <button
                className="secondaryButton"
                onClick={() =>
                  onMovePipeline(row, buildPipelinePayload(nextState, pipelineForm))
                }
                disabled={pendingAction === `PIPELINE-${row.score.id}`}
              >
                Mover a {pipelineStateLabel(nextState)}
              </button>
              {row.pipeline_state && row.pipeline_state !== "LOST" ? (
                <button
                  className="dangerButton"
                  onClick={() =>
                    onMovePipeline(row, buildPipelinePayload("LOST", pipelineForm))
                  }
                  disabled={
                    pendingAction === `PIPELINE-${row.score.id}` ||
                    !pipelineForm.lost_reason.trim()
                  }
                >
                  Marcar perdido
                </button>
              ) : null}
            </div>
          </div>
        ) : (
          <p className="mutedText">Aprueba la empresa antes de moverla por el funnel.</p>
        )}
      </section>

      <section className="detailSection">
        <h3>Borrador</h3>
        {draft && edits ? (
          <div className="draftEditor">
            <label>
              <span>Asunto</span>
              <input
                value={edits.subject}
                onChange={(event) =>
                  setDraftEdits((current) => ({
                    ...current,
                    [draft.id]: { ...edits, subject: event.target.value },
                  }))
                }
              />
            </label>
            <label>
              <span>Cuerpo</span>
              <textarea
                value={edits.body}
                onChange={(event) =>
                  setDraftEdits((current) => ({
                    ...current,
                    [draft.id]: { ...edits, body: event.target.value },
                  }))
                }
              />
            </label>
            <small>Evidencia usada: #{draft.evidence_used.join(", #")}</small>
            <button
              className="secondaryButton"
              onClick={() => onSaveDraft(draft)}
              disabled={pendingAction === `SAVE-${draft.id}`}
            >
              <Save size={16} />
              Guardar borrador
            </button>
          </div>
        ) : (
          <p className="mutedText">Aprueba la empresa antes de generar un borrador editable.</p>
        )}
      </section>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{Math.round(value)}</strong>
    </div>
  );
}

function stateClass(state: string) {
  if (state === "APPROVED" || state === "WON") return "done";
  if (state === "REJECTED" || state === "LOST") return "failed";
  if (state === "QUALIFIED") return "live";
  return "";
}

function nextPipelineState(state: PipelineState | null): PipelineState | null {
  if (state === null) return "APPROVED";
  if (state === "APPROVED") return "CONTACTED";
  if (state === "CONTACTED") return "REPLIED";
  if (state === "REPLIED") return "MEETING";
  if (state === "MEETING") return "PROPOSAL";
  if (state === "PROPOSAL") return "WON";
  return null;
}

function buildPipelinePayload(
  toState: PipelineState,
  form: {
    notes: string;
    channel: "EMAIL" | "LINKEDIN" | "PHONE" | "OTHER";
    message_used: string;
    expected_revenue: string;
    recurring_revenue_monthly: string;
    implementation_revenue: string;
    currency: string;
    lost_reason: string;
  },
) {
  const payload = {
    to_state: toState,
    notes: form.notes || null,
    channel: null as "EMAIL" | "LINKEDIN" | "PHONE" | "OTHER" | null,
    message_used: null as string | null,
    expected_revenue: null as number | null,
    recurring_revenue_monthly: null as number | null,
    implementation_revenue: null as number | null,
    currency: null as string | null,
    lost_reason: null as string | null,
  };
  if (toState === "CONTACTED") {
    payload.channel = form.channel;
    payload.message_used = form.message_used || null;
  }
  if (toState === "WON") {
    payload.expected_revenue = numberOrNull(form.expected_revenue);
    payload.recurring_revenue_monthly = numberOrNull(form.recurring_revenue_monthly);
    payload.implementation_revenue = numberOrNull(form.implementation_revenue);
    payload.currency = form.currency || "EUR";
  }
  if (toState === "LOST") {
    payload.lost_reason = form.lost_reason;
  }
  return payload;
}

function numberOrNull(value: string): number | null {
  const parsed = Number(value);
  return Number.isFinite(parsed) && value.trim() !== "" ? parsed : null;
}
