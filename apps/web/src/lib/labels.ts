export function reviewStateLabel(state: string) {
  const labels: Record<string, string> = {
    RESEARCHED: "Investigado",
    QUALIFIED: "Cualificado",
    APPROVED: "Aprobado",
    REJECTED: "Rechazado",
  };
  return labels[state] ?? state;
}

export function pipelineStateLabel(state: string | null) {
  if (!state) return "Sin iniciar";
  const labels: Record<string, string> = {
    APPROVED: "Aprobado",
    CONTACTED: "Contactado",
    REPLIED: "Respondió",
    MEETING: "Reunión",
    PROPOSAL: "Propuesta",
    WON: "Ganado",
    LOST: "Perdido",
  };
  return labels[state] ?? state;
}

export function researchStateLabel(state: string) {
  const labels: Record<string, string> = {
    DISCOVERED: "Descubierto",
    RESEARCHING: "Investigando",
    RESEARCHED: "Investigado",
    FAILED: "Falló",
  };
  return labels[state] ?? state;
}

export function jobStatusLabel(status: string) {
  const labels: Record<string, string> = {
    queued: "En cola",
    running: "En curso",
    completed: "Completado",
    failed: "Falló",
    idle: "Sin actividad",
  };
  return labels[status] ?? status;
}

export function campaignStatusLabel(status: string) {
  const labels: Record<string, string> = {
    DRAFT: "Borrador",
    RUNNING: "En curso",
    COMPLETED: "Completada",
    FAILED: "Falló",
  };
  return labels[status] ?? status;
}

export function signalLabel(signal: string) {
  const labels: Record<string, string> = {
    PUBLIC_WEBSITE_AVAILABLE: "Web pública disponible",
    HAS_SALES_TEAM: "Equipo comercial visible",
    MULTIPLE_LEAD_CHANNELS: "Varios canales de entrada",
    HAS_CRM: "CRM detectado",
    USES_HUBSPOT: "HubSpot detectado",
    MULTIPLE_LOCATIONS: "Varias ubicaciones",
    MULTIPLE_CONTACT_FORMS: "Varios formularios de contacto",
  };
  return labels[signal] ?? signal.replaceAll("_", " ").toLowerCase();
}
