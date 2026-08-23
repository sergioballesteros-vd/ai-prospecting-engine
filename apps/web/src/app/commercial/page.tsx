"use client";

import { ExternalLink, Loader2, Plus, Save } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { AppShell } from "@/components/AppShell";
import {
  type CommercialAction,
  type CommercialProspect,
  type CommercialScoreboard,
  type CommercialStatus,
  type DiscoveryHypothesis,
  type DiscoverySessionPayload,
  type OutreachTemplate,
  createDiscoverySession,
  getCommercialScoreboard,
  listCommercialProspects,
  listOutreachTemplates,
  recordCommercialAction,
  saveCommercialBuyer,
} from "@/lib/api";

const GROUPS: Array<{ status: CommercialStatus; label: string }> = [
  { status: "TO_CONTACT", label: "TO CONTACT" },
  { status: "CONNECTION_SENT", label: "CONNECTION SENT" },
  { status: "ACCEPTED", label: "ACCEPTED" },
  { status: "REPLIED", label: "REPLIED" },
  { status: "MEETING", label: "MEETING" },
  { status: "PROPOSAL", label: "PROPOSAL" },
  { status: "WON", label: "WON" },
  { status: "LOST", label: "LOST / SKIPPED" },
];

type BuyerForm = { full_name: string; role: string; profile_url: string };

export default function CommercialPage() {
  const [rows, setRows] = useState<CommercialProspect[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [templates, setTemplates] = useState<OutreachTemplate[]>([]);
  const [scoreboard, setScoreboard] = useState<CommercialScoreboard | null>(null);
  const [buyer, setBuyer] = useState<BuyerForm>({ full_name: "", role: "", profile_url: "" });
  const [notes, setNotes] = useState("");
  const [tags, setTags] = useState("");
  const [connectionNote, setConnectionNote] = useState("");
  const [withNote, setWithNote] = useState(true);
  const [pending, setPending] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const selected = useMemo(
    () => rows.find((row) => row.company.id === selectedId) ?? rows[0] ?? null,
    [rows, selectedId],
  );

  useEffect(() => {
    refresh();
  }, []);

  useEffect(() => {
    setBuyer({
      full_name: selected?.buyer?.full_name ?? "",
      role: selected?.buyer?.role ?? "",
      profile_url: selected?.buyer?.profile_url ?? "",
    });
  }, [selected?.company.id, selected?.buyer]);

  async function refresh() {
    setPending("refresh");
    setError(null);
    try {
      const [prospects, reusableTemplates, commercialScoreboard] = await Promise.all([
        listCommercialProspects(),
        listOutreachTemplates(),
        getCommercialScoreboard(),
      ]);
      setRows(prospects);
      setTemplates(reusableTemplates);
      setScoreboard(commercialScoreboard);
      setSelectedId((current) => current ?? prospects[0]?.company.id ?? null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo cargar el inbox comercial");
    } finally {
      setPending(null);
    }
  }

  async function saveBuyer() {
    if (!selected) return;
    if (!buyer.full_name.trim() && !buyer.role.trim()) {
      setError("Añade al menos el nombre o el rol comprador.");
      return;
    }
    setPending("buyer");
    setError(null);
    try {
      const saved = await saveCommercialBuyer(selected.company.id, {
        full_name: buyer.full_name.trim() || null,
        role: buyer.role.trim() || null,
        profile_url: buyer.profile_url.trim() || null,
        channel: "LINKEDIN",
      });
      replaceRow({ ...selected, buyer: saved });
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo guardar el comprador");
    } finally {
      setPending(null);
    }
  }

  async function act(action: CommercialAction) {
    if (!selected) return;
    if ((action === "ADD_NOTE" || action === "MARK_REJECTED") && !notes.trim()) {
      setError("Escribe una nota o motivo antes de guardar esta acción.");
      return;
    }
    setPending(action);
    setError(null);
    try {
      const learningTags = tags
        .split(",")
        .map((item) => item.trim().toLowerCase().replaceAll(" ", "_"))
        .filter(Boolean);
      const updated = await recordCommercialAction(selected.company.id, {
        action,
        opportunity_id: selected.opportunity_id,
        notes: notes.trim() || null,
        channel: "LINKEDIN",
        with_note: action === "MARK_CONNECTION_SENT" ? withNote : null,
        message_used:
          action === "MARK_CONNECTION_SENT" && withNote
            ? connectionNote.trim() || null
            : null,
        message_version: action === "MARK_CONNECTION_SENT" ? "manual-v1" : null,
        evidence_ids: selected.selected_evidence.map((item) => item.id),
        outreach_reason: selected.outreach_reason,
        learning_tags: learningTags,
        lost_reason: action === "MARK_REJECTED" ? notes.trim() : null,
      });
      replaceRow(updated);
      setNotes("");
      setTags("");
      if (action === "MARK_CONNECTION_SENT") setConnectionNote("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo guardar la acción");
    } finally {
      setPending(null);
    }
  }

  function replaceRow(updated: CommercialProspect) {
    setRows((current) =>
      current.map((row) => (row.company.id === updated.company.id ? updated : row)),
    );
    setSelectedId(updated.company.id);
  }

  return (
    <AppShell>
      <section className="workspace">
        <header className="topbar">
          <div>
            <h1>Commercial inbox</h1>
            <p>Operación manual: registra lo que ya hiciste fuera del sistema. Nunca envía mensajes.</p>
          </div>
          <button className="secondaryButton" onClick={refresh} disabled={pending === "refresh"}>
            {pending === "refresh" ? <Loader2 className="spin" size={16} /> : null}
            Actualizar
          </button>
        </header>

        {error ? <div className="notice error">{error}</div> : null}

        {scoreboard ? <CommercialScoreboardView scoreboard={scoreboard} /> : null}

        <section className="commercialGrid">
          <div className="commercialBoard">
            {GROUPS.map((group) => {
              const prospects = rows.filter((row) => row.status === group.status);
              return (
                <section className="commercialGroup" key={group.status}>
                  <header>
                    <strong>{group.label}</strong>
                    <span>{prospects.length}</span>
                  </header>
                  {prospects.map((row) => (
                    <button
                      className={`commercialRow ${
                        selected?.company.id === row.company.id ? "selected" : ""
                      }`}
                      key={row.company.id}
                      onClick={() => setSelectedId(row.company.id)}
                    >
                      <span className="scoreBadge">
                        {row.first_customer_fit
                          ? Math.round(row.first_customer_fit.total_score)
                          : "—"}
                      </span>
                      <span>
                        <strong>{row.company.name}</strong>
                        <small>
                          {row.buyer?.full_name ?? "Comprador sin resolver"}
                          {row.buyer?.role ? ` · ${row.buyer.role}` : ""}
                        </small>
                      </span>
                    </button>
                  ))}
                </section>
              );
            })}
          </div>

          <CommercialDetail
            row={selected}
            buyer={buyer}
            setBuyer={setBuyer}
            notes={notes}
            setNotes={setNotes}
            tags={tags}
            setTags={setTags}
            connectionNote={connectionNote}
            setConnectionNote={setConnectionNote}
            withNote={withNote}
            setWithNote={setWithNote}
            templates={templates}
            pending={pending}
            onSaveBuyer={saveBuyer}
            onAction={act}
            onDiscoverySaved={refresh}
          />
        </section>
      </section>
    </AppShell>
  );
}

function CommercialDetail({
  row,
  buyer,
  setBuyer,
  notes,
  setNotes,
  tags,
  setTags,
  connectionNote,
  setConnectionNote,
  withNote,
  setWithNote,
  templates,
  pending,
  onSaveBuyer,
  onAction,
  onDiscoverySaved,
}: {
  row: CommercialProspect | null;
  buyer: BuyerForm;
  setBuyer: (value: BuyerForm) => void;
  notes: string;
  setNotes: (value: string) => void;
  tags: string;
  setTags: (value: string) => void;
  connectionNote: string;
  setConnectionNote: (value: string) => void;
  withNote: boolean;
  setWithNote: (value: boolean) => void;
  templates: OutreachTemplate[];
  pending: string | null;
  onSaveBuyer: () => void;
  onAction: (action: CommercialAction) => void;
  onDiscoverySaved: () => Promise<void>;
}) {
  if (!row) return <div className="panel empty">No hay prospectos comerciales.</div>;
  const canAct = !["WON", "LOST"].includes(row.status);
  return (
    <article className="panel detailPanel commercialDetail">
      <div className="panelHeader">
        <div>
          <h2>{row.company.name}</h2>
          <p>{row.company.domain}</p>
        </div>
        <span>{commercialStatusLabel(row.status)}</span>
      </div>

      <section className="detailSection commercialSummary">
        <div><span className="label">FirstCustomerFit</span><strong>{row.first_customer_fit ? row.first_customer_fit.total_score.toFixed(1) : "Sin score"}</strong></div>
        <div><span className="label">Última acción</span><strong>{row.last_action}</strong><small>{formatDate(row.last_action_at)}</small></div>
        <div><span className="label">Siguiente acción</span><strong>{row.next_action}</strong></div>
      </section>

      <section className="detailSection">
        <h3>Comprador</h3>
        <div className="buyerGrid">
          <input placeholder="Nombre" value={buyer.full_name} onChange={(event) => setBuyer({ ...buyer, full_name: event.target.value })} />
          <input placeholder="Rol" value={buyer.role} onChange={(event) => setBuyer({ ...buyer, role: event.target.value })} />
          <input placeholder="LinkedIn / perfil URL" value={buyer.profile_url} onChange={(event) => setBuyer({ ...buyer, profile_url: event.target.value })} />
          <button className="secondaryButton" onClick={onSaveBuyer} disabled={pending === "buyer"}><Save size={15} /> Guardar</button>
        </div>
        {row.buyer?.profile_url ? <a className="profileLink" href={row.buyer.profile_url} target="_blank" rel="noreferrer"><ExternalLink size={14} /> Abrir perfil</a> : <p className="mutedText">Perfil no documentado.</p>}
      </section>

      <section className="detailSection">
        <h3>Nota de conexión y evidencia</h3>
        <p className="commercialCopy">{row.connection_note_used ?? (row.connection_note_type === "WITHOUT_NOTE" ? "Enviada sin nota." : "Texto exacto no registrado.")}</p>
        <p className="commercialCopy"><strong>Razón:</strong> {row.outreach_reason ?? "Sin razón seleccionada."}</p>
        {row.selected_evidence.map((item) => <div className="evidenceRow compact" key={item.id}><div className="rowTitle"><span>{item.signal_type}</span><small>#{item.id}</small></div><p>{item.content_excerpt}</p><a href={item.source_url} target="_blank" rel="noreferrer">Fuente pública</a></div>)}
      </section>

      <DiscoverySection row={row} onSaved={onDiscoverySaved} />

      {canAct ? <section className="detailSection commercialActions">
        <h3>Registrar acción manual</h3>
        {row.status === "TO_CONTACT" ? <>
          <label className="checkboxRow"><input type="checkbox" checked={withNote} onChange={(event) => setWithNote(event.target.checked)} /> Con nota</label>
          {withNote ? <textarea maxLength={190} placeholder="Pega la nota realmente enviada (máx. 190)" value={connectionNote} onChange={(event) => setConnectionNote(event.target.value)} /> : null}
          <small>{connectionNote.length}/190</small>
        </> : null}
        <textarea placeholder="Nota manual / motivo de rechazo" value={notes} onChange={(event) => setNotes(event.target.value)} />
        <input placeholder="Learning tags separados por comas" value={tags} onChange={(event) => setTags(event.target.value)} />
        <div className="reviewActions compactActions">
          {row.status === "TO_CONTACT" ? <button onClick={() => onAction("MARK_CONNECTION_SENT")} disabled={Boolean(pending)}>Conexión enviada</button> : null}
          {row.status === "CONNECTION_SENT" ? <><button onClick={() => onAction("MARK_ACCEPTED")} disabled={Boolean(pending)}>Aceptada</button><button className="secondaryButton" onClick={() => onAction("MARK_NO_RESPONSE")} disabled={Boolean(pending)}>Sin respuesta</button></> : null}
          {row.status === "ACCEPTED" ? <button onClick={() => onAction("MARK_REPLIED")} disabled={Boolean(pending)}>Respondió</button> : null}
          {row.status === "REPLIED" || row.status === "ACCEPTED" ? <button onClick={() => onAction("MARK_MEETING")} disabled={Boolean(pending)}>Reunión</button> : null}
          <button className="secondaryButton" onClick={() => onAction("ADD_NOTE")} disabled={Boolean(pending)}>Añadir nota</button>
          <button className="dangerButton" onClick={() => onAction("MARK_REJECTED")} disabled={Boolean(pending)}>Rechazar</button>
        </div>
      </section> : null}

      <section className="detailSection">
        <h3>Aprendizajes</h3>
        <div className="signalsCell">{row.learning_tags.map((tag) => <span key={tag}>{tag.replaceAll("_", " ")}</span>)}</div>
        {row.manual_notes.map((note) => <div className="commercialNote" key={note.id}><p>{note.body}</p><small>{formatDate(note.created_at)}</small></div>)}
      </section>

      <details className="detailSection templateList"><summary>Plantillas reutilizables (copiar y adaptar manualmente)</summary>{templates.map((template) => <section key={template.key}><strong>{template.label}</strong><p>{template.body}</p></section>)}</details>
    </article>
  );
}

const READINESS_DIMENSIONS = [
  ["pain_frequency", "Frecuencia del dolor"],
  ["measurable_baseline", "Baseline medible"],
  ["operational_consequence", "Consecuencia operativa"],
  ["existing_stack_gap", "Gap del stack actual"],
  ["buyer_authority", "Autoridad del buyer"],
  ["workflow_owner_participation", "Participación del owner"],
  ["implementation_simplicity", "Simplicidad"],
  ["willingness_to_change", "Disposición al cambio"],
  ["pilot_safety", "Seguridad del piloto"],
  ["repeatability", "Repetibilidad"],
] as const;

const QUALIFICATION_FIELDS = [
  ["recurring_problem", "Problema recurrente"],
  ["usable_baseline", "Baseline utilizable"],
  ["existing_stack_solves", "El stack actual ya lo resuelve"],
  ["sponsor_confirmed", "Sponsor confirmado"],
  ["workflow_owner_confirmed", "Workflow owner confirmado"],
  ["bounded_safe_pilot", "Piloto acotado y seguro"],
  ["unsafe_requirement", "Requisito inseguro"],
] as const;

type TriState = "unknown" | "yes" | "no";

function CommercialScoreboardView({ scoreboard }: { scoreboard: CommercialScoreboard }) {
  const metrics = [
    ["Conexiones", scoreboard.connections_sent],
    ["Aceptadas", scoreboard.connections_accepted],
    ["Conversaciones", scoreboard.conversations_started],
    ["Discovery calls", scoreboard.discovery_calls],
    ["No problem", scoreboard.no_problem],
    ["Stack resuelve", scoreboard.existing_stack_solves_it],
    ["Measure first", scoreboard.measure_first],
    ["Candidatos laboral", scoreboard.payroll_candidates],
    ["Candidatos extras", scoreboard.out_of_scope_candidates],
    ["Pilot candidates", scoreboard.pilot_candidates],
    ["Pilotos propuestos", scoreboard.pilots_proposed],
    ["Pilotos pagados", scoreboard.pilots_paid],
  ] as const;
  return (
    <section className="discoveryScoreboard" aria-label="Commercial scoreboard">
      <header>
        <div>
          <span className="eyebrow">Objetivo inmediato</span>
          <strong>Primer piloto pagado</strong>
        </div>
        <div className="northStar">
          <span>North Star</span>
          <strong>€{scoreboard.mrr.toFixed(0)} / €{scoreboard.north_star_mrr.toFixed(0)} MRR</strong>
          <small>Setup cobrado: €{scoreboard.setup_revenue.toFixed(0)}</small>
        </div>
      </header>
      <div className="scoreboardMetrics">
        {metrics.map(([label, value]) => <div key={label}><span>{label}</span><strong>{value}</strong></div>)}
      </div>
    </section>
  );
}

function DiscoverySection({
  row,
  onSaved,
}: {
  row: CommercialProspect;
  onSaved: () => Promise<void>;
}) {
  const [open, setOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [hypothesis, setHypothesis] = useState<DiscoveryHypothesis>(
    "PAYROLL_CLOSE_EXCEPTIONS",
  );
  const [discoveryStatus, setDiscoveryStatus] = useState<
    "COMPLETED" | "PARTIAL" | "FOLLOW_UP_REQUIRED"
  >("COMPLETED");
  const [occurredAt, setOccurredAt] = useState(localDateTimeValue);
  const [workflow, setWorkflow] = useState("Cierre mensual laboral y control de excepciones");
  const [software, setSoftware] = useState("");
  const [stackCapability, setStackCapability] = useState("UNKNOWN");
  const [facts, setFacts] = useState("");
  const [painExamples, setPainExamples] = useState("");
  const [objections, setObjections] = useState("");
  const [alternatives, setAlternatives] = useState("");
  const [unresolved, setUnresolved] = useState("");
  const [rawNotes, setRawNotes] = useState("");
  const [nextAction, setNextAction] = useState("");
  const [metrics, setMetrics] = useState<Record<string, string>>({});
  const [workflowDetails, setWorkflowDetails] = useState<Record<string, string>>({});
  const [qualification, setQualification] = useState<Record<string, TriState>>(
    Object.fromEntries(QUALIFICATION_FIELDS.map(([key]) => [key, "unknown"])),
  );
  const [readiness, setReadiness] = useState<Record<string, { score: 0 | 1 | 2; reason: string }>>(
    Object.fromEntries(
      READINESS_DIMENSIONS.map(([key]) => [key, { score: 1, reason: "No evaluado en esta sesión" }]),
    ),
  );

  const latest = row.discovery_sessions[0] ?? null;
  const calculationPreview = useMemo(() => {
    const suppliedTotal = optionalNumber(metrics.total_followup_minutes);
    const reminders = optionalNumber(metrics.manual_reminders);
    const minutesEach = optionalNumber(metrics.minutes_per_reminder);
    const total = suppliedTotal ?? (reminders !== null && minutesEach !== null ? reminders * minutesEach : null);
    const hours = total === null ? null : total / 60;
    const hourlyCost = optionalNumber(metrics.buyer_hourly_cost);
    return {
      total,
      hours,
      cost: hours !== null && hourlyCost !== null ? hours * hourlyCost : null,
    };
  }, [metrics]);

  function setMetric(name: string, value: string) {
    setMetrics((current) => ({ ...current, [name]: value }));
  }

  function setWorkflowDetail(name: string, value: string) {
    setWorkflowDetails((current) => ({ ...current, [name]: value }));
  }

  function switchHypothesis(value: DiscoveryHypothesis) {
    setHypothesis(value);
    setWorkflow(
      value === "PAYROLL_CLOSE_EXCEPTIONS"
        ? "Cierre mensual laboral y control de excepciones"
        : value === "OUT_OF_SCOPE_WORK"
          ? "Solicitud extra → alcance → aprobación → ejecución → facturación"
          : "Otro workflow observado",
    );
  }

  async function saveSession() {
    if (!workflow.trim() || !nextAction.trim()) {
      setFormError("Describe el workflow y guarda una siguiente acción concreta.");
      return;
    }
    setSaving(true);
    setFormError(null);
    try {
      const buyerMetrics = Object.fromEntries(
        Object.entries(metrics)
          .map(([key, value]) => [key, optionalNumber(value)] as const)
          .filter((entry): entry is [string, number] => entry[1] !== null),
      );
      const qualificationPayload = Object.fromEntries(
        Object.entries(qualification).map(([key, value]) => [key, triStateValue(value)]),
      );
      delete qualificationPayload.work_before_pricing;
      qualificationPayload.out_of_scope_example_confirmed =
        hypothesis === "OUT_OF_SCOPE_WORK"
          ? qualificationPayload.out_of_scope_example_confirmed ?? null
          : null;
      await createDiscoverySession(row.company.id, {
        contact_id: row.buyer?.id ?? null,
        opportunity_id: row.opportunity_id,
        occurred_at: new Date(occurredAt).toISOString(),
        hypothesis,
        workflow_discussed: workflow.trim(),
        discovery_status: discoveryStatus,
        existing_software: splitEntries(software),
        workflow_details: {
          ...Object.fromEntries(
            Object.entries(workflowDetails)
              .filter(([, value]) => value.trim())
              .map(([key, value]) => [
                key,
                ["real_client_channels", "spreadsheets_side_systems"].includes(key)
                  ? splitEntries(value)
                  : value.trim(),
              ]),
          ),
          work_before_pricing:
            hypothesis === "OUT_OF_SCOPE_WORK"
              ? triStateValue(qualification.work_before_pricing ?? "unknown")
              : null,
        },
        buyer_reported_facts: splitLines(facts),
        buyer_reported_metrics: buyerMetrics,
        pain_examples: splitLines(painExamples),
        objections: splitLines(objections),
        alternatives: splitLines(alternatives),
        existing_stack_capability: stackCapability,
        qualification: qualificationPayload,
        readiness,
        unresolved_questions: splitLines(unresolved),
        next_action: nextAction.trim(),
        raw_notes: rawNotes.trim() || null,
      } as DiscoverySessionPayload);
      setOpen(false);
      await onSaved();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "No se pudo guardar la sesión");
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="detailSection discoverySection">
      <div className="sectionTitleRow">
        <div>
          <h3>Discovery lab</h3>
          <p>Buyer-reported; separado de la evidencia pública.</p>
        </div>
        <button className="secondaryButton" onClick={() => setOpen((value) => !value)}>
          <Plus size={15} /> Nueva sesión
        </button>
      </div>

      {latest ? <article className="discoveryResult">
        <header>
          <span className={`outcomeBadge outcome-${latest.qualification_outcome.toLowerCase()}`}>
            {latest.qualification_outcome.replaceAll("_", " ")}
          </span>
          <small>{formatDate(latest.occurred_at)} · readiness {latest.readiness_total}/20</small>
        </header>
        <p><strong>Workflow:</strong> {latest.workflow_discussed}</p>
        <p><strong>Siguiente acción:</strong> {latest.next_action}</p>
        {latest.fatal_blockers.length ? <div className="blockerList">{latest.fatal_blockers.map((item) => <span key={item}>{item.replaceAll("_", " ")}</span>)}</div> : <p className="greenText">Sin blockers fatales registrados.</p>}
        {Object.entries(latest.calculated_metrics).map(([key, item]) => <div className="calculationRow" key={key}><strong>{key.replaceAll("_", " ")}: {item.value} {item.unit}</strong><small>{item.formula}</small></div>)}
        {latest.missing_information.length ? <details><summary>Información pendiente ({latest.missing_information.length})</summary><p>{latest.missing_information.join(" · ")}</p></details> : null}
      </article> : <p className="mutedText">Aún no hay discovery real registrado. No se ha inferido ninguna sesión desde outreach.</p>}

      {open ? <div className="discoveryForm">
        {formError ? <div className="notice error">{formError}</div> : null}
        <div className="discoveryCoreGrid">
          <label>Hipótesis<select value={hypothesis} onChange={(event) => switchHypothesis(event.target.value as DiscoveryHypothesis)}><option value="PAYROLL_CLOSE_EXCEPTIONS">Cierre laboral</option><option value="OUT_OF_SCOPE_WORK">Trabajo fuera de alcance</option><option value="OTHER_WORKFLOW">Otro workflow</option></select></label>
          <label>Capacidad del stack<select value={stackCapability} onChange={(event) => setStackCapability(event.target.value)}><option value="UNKNOWN">Desconocida</option><option value="SOLVES_WITH_REASONABLE_CONFIGURATION">Ya lo resuelve</option><option value="CONFIGURATION_GAP">Gap de configuración</option><option value="ADOPTION_GAP">Gap de adopción</option><option value="FUNCTIONALITY_GAP">Falta funcionalidad</option></select></label>
          <label>Fecha de la conversación<input type="datetime-local" value={occurredAt} onChange={(event) => setOccurredAt(event.target.value)} /></label>
          <label>Estado de la sesión<select value={discoveryStatus} onChange={(event) => setDiscoveryStatus(event.target.value as "COMPLETED" | "PARTIAL" | "FOLLOW_UP_REQUIRED")}><option value="COMPLETED">Completada</option><option value="PARTIAL">Parcial</option><option value="FOLLOW_UP_REQUIRED">Requiere follow-up</option></select></label>
        </div>
        <label>Workflow discutido<input value={workflow} onChange={(event) => setWorkflow(event.target.value)} /></label>
        <label>Software existente (comas)<input placeholder="A3, Sage, Bilky, Excel…" value={software} onChange={(event) => setSoftware(event.target.value)} /></label>
        <div className="discoveryCoreGrid">
          {hypothesis === "PAYROLL_CLOSE_EXCEPTIONS" ? <>
            <WorkflowInput label="Cutoff real" name="cutoff" values={workflowDetails} onChange={setWorkflowDetail} />
            <WorkflowInput label="Portal y uso real" name="portal" values={workflowDetails} onChange={setWorkflowDetail} />
            <WorkflowInput label="Canales reales (comas)" name="real_client_channels" values={workflowDetails} onChange={setWorkflowDetail} />
            <WorkflowInput label="Excel/sistemas laterales" name="spreadsheets_side_systems" values={workflowDetails} onChange={setWorkflowDetail} />
            <WorkflowInput label="Owner de excepciones" name="exception_owner" values={workflowDetails} onChange={setWorkflowDetail} />
            <WorkflowInput label="Cómo se conoce el estado" name="status_visibility_method" values={workflowDetails} onChange={setWorkflowDetail} />
          </> : hypothesis === "OUT_OF_SCOPE_WORK" ? <>
            <WorkflowInput label="Canales de solicitud" name="real_client_channels" values={workflowDetails} onChange={setWorkflowDetail} />
            <WorkflowInput label="Cómo se comprueba el scope" name="scope_check_method" values={workflowDetails} onChange={setWorkflowDetail} />
            <WorkflowInput label="Quién aprueba" name="approval_owner" values={workflowDetails} onChange={setWorkflowDetail} />
            <WorkflowInput label="Cómo se registra" name="out_of_scope_recording_method" values={workflowDetails} onChange={setWorkflowDetail} />
            <WorkflowInput label="Handoff a facturación" name="invoice_handoff" values={workflowDetails} onChange={setWorkflowDetail} />
            <WorkflowInput label="Revisión de rentabilidad" name="profitability_review" values={workflowDetails} onChange={setWorkflowDetail} />
            <label>¿Se ejecuta antes de poner precio?<select value={qualification.work_before_pricing ?? "unknown"} onChange={(event) => setQualification((current) => ({ ...current, work_before_pricing: event.target.value as TriState }))}><option value="unknown">Desconocido</option><option value="yes">Sí</option><option value="no">No</option></select></label>
          </> : null}
        </div>
        <label>Último caso real / hechos del buyer (una línea por hecho)<textarea value={facts} onChange={(event) => setFacts(event.target.value)} /></label>
        <label>Ejemplos de dolor y consecuencia<textarea value={painExamples} onChange={(event) => setPainExamples(event.target.value)} /></label>

        <div className="discoveryMetricsGrid">
          {hypothesis === "PAYROLL_CLOSE_EXCEPTIONS" ? <>
            <MetricInput label="Empresas en nómina" name="client_companies_payroll" values={metrics} onChange={setMetric} />
            <MetricInput label="Empleados procesados" name="employees_processed" values={metrics} onChange={setMetric} />
            <MetricInput label="Adopción portal (%)" name="portal_adoption_percent" values={metrics} onChange={setMetric} />
            <MetricInput label="Empresas con recordatorio" name="companies_requiring_reminders" values={metrics} onChange={setMetric} />
            <MetricInput label="Recordatorios manuales" name="manual_reminders" values={metrics} onChange={setMetric} />
            <MetricInput label="Minutos / recordatorio" name="minutes_per_reminder" values={metrics} onChange={setMetric} />
            <MetricInput label="Minutos totales (si se midieron)" name="total_followup_minutes" values={metrics} onChange={setMetric} />
            <MetricInput label="Incompletas al corte" name="incomplete_at_cutoff" values={metrics} onChange={setMetric} />
            <MetricInput label="Cambios tardíos" name="late_changes" values={metrics} onChange={setMetric} />
            <MetricInput label="Correcciones/reaperturas trimestre" name="corrections_reopens_last_quarter" values={metrics} onChange={setMetric} />
            <MetricInput label="Coste/hora dado por buyer (€)" name="buyer_hourly_cost" values={metrics} onChange={setMetric} />
            <MetricInput label="Personas involucradas" name="people_involved" values={metrics} onChange={setMetric} />
          </> : hypothesis === "OUT_OF_SCOPE_WORK" ? <>
            <MetricInput label="Ejemplos últimos 90 días" name="out_of_scope_examples_90d" values={metrics} onChange={setMetric} />
            <MetricInput label="Valor estimado por buyer (€)" name="out_of_scope_estimated_value" values={metrics} onChange={setMetric} />
            <MetricInput label="Valor facturado (€)" name="out_of_scope_invoiced_value" values={metrics} onChange={setMetric} />
            <MetricInput label="Retraso factura (días)" name="invoice_delay_days" values={metrics} onChange={setMetric} />
          </> : null}
        </div>

        {hypothesis === "PAYROLL_CLOSE_EXCEPTIONS" && calculationPreview.hours !== null ? <div className="calculationPreview"><span>Seguimiento: <strong>{calculationPreview.hours.toFixed(2)} h/mes</strong></span>{calculationPreview.cost !== null ? <span>Coste estimado: <strong>€{calculationPreview.cost.toFixed(2)}/mes</strong></span> : <span>Coste: falta coste/hora del buyer</span>}<small>{calculationPreview.total} min ÷ 60; no se han rellenado ausencias con cero.</small></div> : null}

        <div className="qualificationGrid">
          {QUALIFICATION_FIELDS.map(([key, label]) => <label key={key}>{label}<select value={qualification[key]} onChange={(event) => setQualification((current) => ({ ...current, [key]: event.target.value as TriState }))}><option value="unknown">Desconocido</option><option value="yes">Sí</option><option value="no">No</option></select></label>)}
          {hypothesis === "OUT_OF_SCOPE_WORK" ? <label>Ejemplo buyer-reported confirmado<select value={qualification.out_of_scope_example_confirmed ?? "unknown"} onChange={(event) => setQualification((current) => ({ ...current, out_of_scope_example_confirmed: event.target.value as TriState }))}><option value="unknown">Desconocido</option><option value="yes">Sí</option><option value="no">No</option></select></label> : null}
        </div>

        <details className="discoveryDetails"><summary>Assessment 0–2 y notas complementarias</summary>
          <div className="readinessGrid">{READINESS_DIMENSIONS.map(([key, label]) => <div key={key}><label>{label}<select value={readiness[key].score} onChange={(event) => setReadiness((current) => ({ ...current, [key]: { ...current[key], score: Number(event.target.value) as 0 | 1 | 2 } }))}><option value={0}>0 · ausente</option><option value={1}>1 · débil/desconocido</option><option value={2}>2 · confirmado</option></select></label><input aria-label={`Razón: ${label}`} value={readiness[key].reason} onChange={(event) => setReadiness((current) => ({ ...current, [key]: { ...current[key], reason: event.target.value } }))} /></div>)}</div>
          <label>Objeciones<textarea value={objections} onChange={(event) => setObjections(event.target.value)} /></label>
          <label>Alternativas actuales<textarea value={alternatives} onChange={(event) => setAlternatives(event.target.value)} /></label>
          <label>Preguntas sin resolver<textarea value={unresolved} onChange={(event) => setUnresolved(event.target.value)} /></label>
          <label>Notas crudas<textarea value={rawNotes} onChange={(event) => setRawNotes(event.target.value)} /></label>
        </details>
        <label>Siguiente acción<input placeholder="Medir un cierre / activar portal / segunda llamada…" value={nextAction} onChange={(event) => setNextAction(event.target.value)} /></label>
        <button onClick={saveSession} disabled={saving}>{saving ? <Loader2 className="spin" size={16} /> : <Save size={16} />} Guardar sesión histórica</button>
      </div> : null}

      {row.discovery_sessions.length > 1 ? <details className="discoveryHistory"><summary>Historial ({row.discovery_sessions.length})</summary>{row.discovery_sessions.map((session) => <div key={session.id}><strong>{session.qualification_outcome.replaceAll("_", " ")}</strong><span>{formatDate(session.occurred_at)}</span><p>{session.next_action}</p></div>)}</details> : null}
    </section>
  );
}

function MetricInput({
  label,
  name,
  values,
  onChange,
}: {
  label: string;
  name: string;
  values: Record<string, string>;
  onChange: (name: string, value: string) => void;
}) {
  return <label>{label}<input type="number" min="0" step="any" value={values[name] ?? ""} onChange={(event) => onChange(name, event.target.value)} /></label>;
}

function WorkflowInput({
  label,
  name,
  values,
  onChange,
}: {
  label: string;
  name: string;
  values: Record<string, string>;
  onChange: (name: string, value: string) => void;
}) {
  return <label>{label}<input value={values[name] ?? ""} onChange={(event) => onChange(name, event.target.value)} /></label>;
}

function optionalNumber(value: string | undefined): number | null {
  if (value === undefined || value.trim() === "") return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function localDateTimeValue(): string {
  const now = new Date();
  return new Date(now.getTime() - now.getTimezoneOffset() * 60_000).toISOString().slice(0, 16);
}

function triStateValue(value: TriState): boolean | null {
  return value === "yes" ? true : value === "no" ? false : null;
}

function splitLines(value: string): string[] {
  return value.split("\n").map((item) => item.trim()).filter(Boolean);
}

function splitEntries(value: string): string[] {
  return value.split(/[\n,]/).map((item) => item.trim()).filter(Boolean);
}

function commercialStatusLabel(status: CommercialStatus) {
  return GROUPS.find((group) => group.status === status)?.label ?? status;
}

function formatDate(value: string | null) {
  return value ? new Date(value).toLocaleString("es-ES") : "Fecha no registrada";
}
