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
    OWNER_LED: "Dirección propietaria visible",
    MANAGING_PARTNER_VISIBLE: "Socio responsable visible",
    SMALL_LOCAL_TEAM: "Equipo local pequeño",
    STANDARD_VERTICAL_SOFTWARE: "Software vertical estándar",
    MULTIPLE_ADVISORY_AREAS: "Varias áreas de asesoría",
    DOCUMENT_HEAVY_WORKFLOW: "Flujo intensivo en documentos",
    CLIENT_INTAKE_FLOW: "Entrada de cliente visible",
    MANUAL_HANDOFF_HYPOTHESIS: "Hipótesis de traspasos manuales",
    DIRECT_CONTACT_PATH: "Contacto directo",
    LOCAL_OFFICE: "Oficina local",
    NO_INTERNAL_TECH_TEAM_VISIBLE: "Sin equipo técnico visible",
    PROPRIETARY_ERP: "ERP propio",
    PROPRIETARY_PLATFORM: "Plataforma propia",
    SELLS_TECH_TO_OTHER_FIRMS: "Vende tecnología a asesorías",
    INTERNAL_PRODUCT_TEAM: "Equipo de producto interno",
    INTERNAL_ENGINEERING_TEAM: "Equipo de ingeniería interno",
    EXPLICIT_AI_AUTOMATION_PROGRAM: "Automatización/IA explícita",
    ENTERPRISE_SCALE: "Escala enterprise",
    MULTINATIONAL_COMPLEXITY: "Complejidad multinacional",
    LONG_PROCUREMENT_RISK: "Riesgo de procurement largo",
  };
  return labels[signal] ?? signal.replaceAll("_", " ").toLowerCase();
}
