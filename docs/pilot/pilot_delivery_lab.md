# Pilot Delivery Lab — first paid payroll-close exception pilot

Research cut-off: **2026-08-23**. Status: pre-implementation architecture only. No connector, integration, credential, deployment, contact or production change is authorized.

## Executive decision

The likely first pilot can and should be delivered **without writing to the payroll system**.

Recommended default:

> Configure the customer’s existing portal/email/form capabilities first. Represent only the validated monthly-close workflow in a customer-owned, metadata-only exception queue. Use deterministic completeness rules, named owners, bounded approved reminder candidates, human review and manual payroll handoff. Do not use an LLM or ERP API unless a measured residual gap justifies it.

This is **Blueprint A0**. It can fit approximately **3–7 working days** for one engineer when access, cohort, checklist, baseline, templates and owners are ready. The €1,000 setup price is **conditional**: reasonable around 18–35 hours, deliberately subsidized at the margin up to roughly 35–45, and incompatible with unknown APIs, broad mailbox OAuth, OCR, RPA or write-back.

## Scope boundary

In scope:

- One monthly payroll-close input/completeness workflow.
- One payroll product/version/environment.
- One client-company cohort and one close.
- Approved corporate form, portal, shared/collaborative mailbox or dedicated route.
- Metadata/status, owners, deadlines, exception codes and source references.
- Firm-owned templates and human-approved communication.
- Manual handoff to the payroll system.

Out of scope:

- Payroll calculation, salaries, legal/labor conclusions, government filing or automated employee-status decisions.
- Multi-ERP, multi-tenant SaaS, universal connectors, OCR platform, chatbot, CRM or generic workflow builder.
- Personal WhatsApp, free-form autonomous replies, shared passwords, RPA/browser scraping or direct vendor database access.
- Payroll-system write-back. Current decision: `NO_SAFE_WRITEBACK_RECOMMENDED`.

## Existing-stack-first findings

Every prospect starts with: **Can the software already solve this by configuration, activation or workflow change?**

| Product | Confirmed existing-stack opportunities | API position | Delivery implication |
|---|---|---|---|
| A3 / Wolters Kluwer | a3asesor Nom process alerts/task review; a3HRgo/a3innuva portal for documents, requests, data updates and plan-dependent payroll inputs. | Official cloud a3innuva Nómina REST API exists with Conectia and vendor-provisioned OAuth; not on-prem. Restricted task/company access exists, but published changelog says read/write permissions are not separated. Payroll webhooks/generic safe task write not found. | Configure portal/tasks first. Blueprint B only for exact cloud+Conectia case with accepted credential risk and separate economics. |
| Sage Despachos Connected | Internal cases/tasks/workloads/request tracking, labor alerts/comments, portal/document modules and Excel exports. | Public Despachos payroll API/OAuth/webhooks/safe write not found. Sage 200 and generic Sage APIs do not prove Despachos payroll support. | Strong `CONFIGURE_EXISTING_STACK`; use vendor/partner or supported Excel handoff. |
| Bilky | Advisor/company/employee portals, forms/fields, tickets, alerts, roles, documents, history and import/export. | Connectors are marketed; public API/auth/webhooks/limits not found. | Native configuration is the closest fit and may eliminate the need for custom software. |
| Cegid/Diez | DiezNOM portal documents, messages, requests and notifications. | Public Diez API/export contract/webhooks/safe write not found. | Configure portal + existing task/Excel; validate with Diez support before estimating any bridge. |
| Aplifisa | Portal incidents/request status, Doc3W, email notices, labor Excel reports and support path. | Public Laboral API/OAuth/webhooks/safe write not found. | Configure portal/Doc3W/Excel first; a stable supported export can enable B-lite. |

Detailed facts, uncertainty and official URLs are in [pilot_stack_matrix.md](./pilot_stack_matrix.md) and [pilot_vendor_sources.md](./pilot_vendor_sources.md).

## Smallest useful exception queue

The queue is an operational close checklist, not a CRM and not an employee record system.

### Required fields

| Field | Rule |
|---|---|
| `client_company_id`, `client_company_name` | Stable customer-owned company identity; exact mapping only. |
| `payroll_period` | Explicit period; part of uniqueness key. |
| `request_status` | Controlled state, not prose. |
| `completeness_status` | Derived from versioned required-item codes; `COMPLETE` is not payroll/legal approval. |
| `exception_type`, `missing_items` | Small controlled taxonomy/list. |
| `source_channel`, `source_references` | Provider + opaque message/form/portal IDs or access-controlled links; avoid body/bytes. |
| `owner`, `next_action`, `due_date` | One accountable operator and explicit cutoff action. |
| `last_contact_at`, `reminder_count`, `buyer_client_response_status` | Communication control and suppression. |
| `human_review_status` | Separate deterministic completeness from approval. |
| timestamps/checklist version | Created/updated/approved/handed-off/closed plus append-only events. |

States: `NOT_REQUESTED → REQUESTED → PARTIAL/COMPLETE → NEEDS_REVIEW/BLOCKED → APPROVED → HANDED_OFF → CLOSED`. Only a human can set `APPROVED`; `BLOCKED` never advances automatically. The state diagram and invariants are in [pilot_architecture_blueprints.md](./pilot_architecture_blueprints.md).

### Do not store

Salary, bank account, national/tax/Social Security IDs, addresses, dependants, health/IT details, union/garnishment/disciplinary information, contracts, collective-agreement interpretations, payroll calculations, payroll PDFs, whole email bodies, attachments, external credentials, or “useful later” fields. Employee name should be avoided where a customer-owned reference works. Any unavoidable sensitive/special-category/document processing triggers security review and re-estimation.

## Reminder design

### Safety contract

- Firm approves and versions every template.
- Firm owns the sender/account and communication relationship.
- v1 creates a **reminder candidate**; a human reviews/approves and the firm sends it.
- Candidate contains only controlled variables: company display name, period, missing-item labels, due date and firm contact.
- Stop on complete, stop flag, ambiguous/contradictory response, `BLOCKED`, maximum count or cutoff.
- Cadence and maximum are fixed before the close; no adaptive “AI” cadence.
- Manual override and kill switch are immediate and audited.
- No personal WhatsApp. WhatsApp Business is excluded from v1; it would require official API, corporate number, approved business purpose/channel, DPA/subprocessors, consent/retention design and separate economics.

### Channel comparison

| Mechanism | Safety/value | v1 decision |
|---|---|---|
| Existing payroll/client portal reminder | Keeps data/identity/history in the paid system; may already expose status/notifications | **First choice** when licensed and configurable; vendor/partner owns setup. |
| Manual reminder queue | Maximum control, easy rollback, no send permission; modest labor remains | **Default cross-stack choice.** |
| Email-only through shared/collaborative mailbox | Familiar and auditable in customer tenant; risk of mixed messages/attachments and duplicated sends | **Acceptable** with dedicated route, approved templates, human send and sent-item reconciliation. |
| Power Automate/Apps Script | Can create candidates/scheduled views; ownership/licensing/trigger reliability require controls | **Conditional configuration**, customer-owned; do not auto-send in v1. |
| Custom Graph/Gmail API | Enables reliable metadata ingestion when implemented with reconciliation; adds OAuth, scopes, verification and maintenance | **Conditional A1**, only after residual gap. |
| Approved messaging platform / WhatsApp Business | Useful only for buyer-required corporate channel with full governance | **Not v1.** Personal WhatsApp **rejected**. |

Microsoft documents shared-mailbox Power Automate duplicate/missed/attachment limitations; Google push uses Pub/Sub, seven-day watch renewal and history reconciliation. Therefore notifications are hints, not source-of-truth completion signals.

## LLM decision

**An LLM is not necessary for the first pilot.** The safest pilot uses a form or controlled subject/template, a deterministic checklist and human review.

| Possible use | Classification | v1 rule |
|---|---|---|
| Classify approved form/status or known subject token | **Deterministic rule sufficient** | Use allowlisted values/regex/mapping. |
| Identify missing required items from structured fields | **Deterministic rule sufficient** | Versioned checklist; no model. |
| Classify messy free-text into a small exception category | **LLM optional** | Only after measuring rule failure; output is suggestion with confidence/evidence, human confirms. |
| Extract a few fields from free-text email | **LLM optional/useful only if volume and variability prove need** | Minimize/redact input; strict schema; no attachment by default; human confirms ambiguous result. |
| Summarize a long email thread | **LLM useful but not necessary** | Human convenience only; source remains authoritative; never drives state alone. |
| Suggest exception category | **LLM optional** | Suggestion only; no automatic approval/reminder. |
| Determine legal sufficiency, employment status, agreement interpretation, payroll result or filing | **LLM not appropriate** | Prohibited. |
| Draft/send autonomous client reply | **LLM not appropriate** | Prohibited; templates + human send. |

If later enabled, require approved provider/DPA/subprocessors/region/retention/training settings, minimum input, strict schema, evidence/source IDs, uncertainty threshold, prompt-injection isolation, cost logs and deterministic/manual fallback. Any ambiguity fails to `NEEDS_REVIEW`.

## Data protection and security recommendation

Expected role pattern is customer/advisory firm as controller and Sergio as processor, but roles follow actual purposes/means and must be confirmed. Before production data: DPA, lawful instructions, processing inventory, risk assessment/DPIA decision, subprocessor/region/transfer list, access/incident/retention/deletion/offboarding plan, and synthetic test data.

Default controls:

- Customer corporate identity/MFA, named operators and least privilege.
- Dedicated input route; no general mailbox or personal accounts.
- Customer-owned configuration when possible.
- Single-customer service/database if A1 is necessary; no immature `tenant_id` multi-tenancy.
- TLS, managed encryption at rest, secret store, scrubbed logs and append-only audit.
- No documents; transient attachment handling only after type/size/malware controls and explicit need.
- Paid tested backups if a database is used; code rollback and data restore are separate.
- Independent kill switches for intake, reminders, LLM and ERP read.
- Export/revocation/deletion tested before close.

The full checklist and security-review triggers are in [pilot_security_checklist.md](./pilot_security_checklist.md).

## Deployment options

| Option | Simplicity/isolation/operations | Cost shape | Recommendation |
|---|---|---|---|
| Customer M365/Google tenant only | Simplest; identity, file/form/mail retention and ownership stay customer-side; revision history may be sufficient for low-risk A0 | Usually existing licenses; verify Power Automate/Vault/Purview/module entitlements | **Default A0.** No deployment if it works. |
| Existing Prospecting Engine service/database | Technically familiar but mixes sales/research and employee/payroll-adjacent purposes; current coarse API-token/in-process job pattern is not sufficient final isolation/auth | Low incremental hosting, high governance coupling | **Reject shared production/data store.** Reuse conventions only. |
| Dedicated small pilot service + Postgres | Clear one-client isolation, logs, audit, rollback and deletion; adds hosting/auth/backup/support | Small paid service/database; use Frankfurt and paid backup | **Conditional A1 default** when custom runtime is proven necessary. |
| Serverless function/worker | Good for brief events but auth/webhook/scheduling/observability and cold starts can fragment a tiny system | Low usage cost, higher operational pieces | **Not default.** Use only if customer platform already standardizes it. |
| Scheduled job/cron | Fits daily review/cutoff; idempotent job plus manual fallback is enough | Minimal; Render cron has small monthly minimum | **Use one only if A1 needs it.** No queue system. |
| Redis/Celery/message queue | Adds retry/worker topology but little value at one cohort/close | More infrastructure/support | **Reject for v1.** |

For a dedicated Render option, official docs confirm Frankfurt, Postgres encryption, paid backups/PITR, health checks, deploy rollback and cron. The current repository’s FastAPI/SQLAlchemy/Postgres conventions are reusable, but not its production data or deployment. Do not deploy until the hard gate is complete.

## Blueprint decisions

- **A — no ERP:** **YES / DEFAULT.** 18–35 hours typical for configuration/small bridge; safe in 3–7 days when prerequisites are ready.
- **B — read-only ERP:** **CONDITIONAL.** Only official cloud a3innuva Nómina currently has enough public contract to design API access, and its lack of read/write permission separation is a risk. Supported file exports can enable B-lite. Benefit must be measured and separately priced.
- **C — limited write:** `NO_SAFE_WRITEBACK_RECOMMENDED`. No reviewed product exposes a clearly documented, separately permissioned, bounded non-payroll task/note write suitable for this offer.

## No-API fallback and RPA

Fallback order across vendors: configure native portal/task/alerts → customer form/shared inbox → supported CSV/Excel/report → manual review/handoff → vendor/authorized partner connector → no integration. Detailed per-vendor paths are in [pilot_stack_matrix.md](./pilot_stack_matrix.md).

RPA classification:

- **REJECTED** for payroll writes, shared passwords, private endpoints, direct database access or normal pilot delivery.
- **LAST_RESORT** only for a vendor-approved read-only export when no supported export/API exists, a test environment and written approval exist, UI changes are monitored, failure is visible, and economics are re-scoped.
- **ACCEPTABLE:** none identified for the default first pilot. A vendor-owned/supported automation is a vendor integration, not Sergio’s brittle RPA.

## Delivery and profitability

Blueprint A setup by stack is generally **GOOD FIT** for A3+M365, A3+Google, Sage, Bilky configuration and a well-defined Aplifisa setup; Cegid/Diez is **CONDITIONAL** because export/task details need support confirmation. Any API B outside an already entitled/documented a3 cloud case is **BAD FIT** until official access exists. Blueprint C is **BAD FIT**.

The first-month support target is usually 2–6 hours for A0/A1, then 1–3 hours/month if stable. If Sergio must manually operate the queue, repair mappings, chase clients, handle repeated OAuth/vendor changes, or provide general IT support, €200/month is incompatible.

Full ranges and uncertainties are in [pilot_stack_matrix.md](./pilot_stack_matrix.md). Refusal/recommend-third-party rules are in [pilot_economic_kill_criteria.md](./pilot_economic_kill_criteria.md).

## What not to build

Reject now: universal A3 connector, universal Sage connector, universal payroll abstraction, multi-tenant SaaS, OCR engine, general email classifier, chatbot, generic workflow builder, WhatsApp automation platform, payroll engine, legal decision agent, customer mobile app, full CRM, custom portal, browser RPA, event bus/Redis/Celery/microservices and default LLM pipeline. Each either duplicates current vendors, expands sensitive data/liability, or cannot be supported at the offer economics.

## Operational failure posture

The practical matrix in [pilot_failure_modes.md](./pilot_failure_modes.md) covers revoked permissions, API/ERP outage, duplicate/missed email, unreadable/malicious attachment, incomplete/contradictory input, owner absence, cutoff, wrong/duplicate reminder, LLM uncertainty/injection, mapping/client changes, credential/API changes, spreadsheet corruption, deployment/backup/audit failure, data-category breach and customer non-adoption.

Resume after a material failure only when cause/range are known, access/integrity is verified, source-to-queue reconciliation is complete, reminder risk is reviewed, regression tests pass and the workflow owner approves.

## Final decisions

### A — Can the likely first pilot be delivered without writing to the payroll system?

**YES.** The default should have no payroll credentials at all. Manual handoff is a feature, not a temporary defect.

### B — Can the safest default pilot be delivered in approximately 3–7 working days by one engineer?

**DEPENDS.** It is achievable when the handoff and customer access are complete, one checklist/cohort/close is frozen, customer-owned tools are used, storage is metadata-only and there is no custom ERP/API work. If any of those prerequisites fail, re-scope rather than promise seven days.

### C — Is €1,000 setup commercially compatible?

**CONDITIONAL.** Compatible for roughly 18–35 hours of A0/small A1 delivery. It is not compatible with Blueprint B API build, unknown vendor access, restricted-scope verification/security assessment, OCR/RPA or Blueprint C. Do not let a design-partner subsidy become the standard unit economics.

### D — Which stack is easiest for the first case?

Based only on verified configuration/integration evidence for this workflow:

1. **Bilky**
2. **Sage Despachos Connected**
3. **Aplifisa**
4. **A3 / Wolters Kluwer**
5. **Cegid/Diez**

A3 moves to first for a separately priced Blueprint B only when discovery confirms cloud a3innuva Nómina + Conectia + vendor-issued OAuth and the customer accepts the read/write permission limitation. Ranking is not a reason to sell: if native configuration solves the problem, the outcome is `EXISTING_STACK_SOLVES_IT`.

### E — Recommended default architecture

**Blueprint A0: customer-owned approved form/portal/shared inbox → deterministic metadata checklist → narrow exception queue → owner/reminder candidate → human review → manual payroll-system handoff, with audit and manual fallback. No ERP write, no LLM, no document store, no custom deployment unless a measured residual gap remains.**

### F — Exact discovery facts that make us refuse implementation

- Multiple payroll systems/workflows/cohorts/closes or non-isolatable workflow.
- Payroll calculation, filing, salary/legal/employee-status decision or automated payroll write.
- Personal WhatsApp, personal/general mailbox, shared password, unrestricted domain/mail access, private API, direct DB or RPA dependency.
- No sponsor, owner, reviewer, backup, cutoff, baseline, target, rehearsal or manual fallback.
- Existing licensed stack solves it and buyer refuses that cheaper path.
- Required sensitive/special-category/document processing exceeds approved security/legal capability or economics.
- Customer refuses DPA, data minimization, least privilege, audit, retention/deletion, incident duties, access revocation or human approval.
- Undocumented API/export, long vendor certification/partner approval, no test path, or no stable exact identifiers.
- Estimate exceeds roughly 35–45 hours at €1,000 without a change order, or expected support exceeds the €200/month boundary.
- Customer expects autonomous communication, unlimited changes, general IT support or an SLA current capability cannot meet.
- Any ambiguity cannot fail closed before payroll impact.

## Next valid action

Implementation is authorized only by `PILOT_CANDIDATE` + completed `pilot_candidate_handoff` + Sergio’s explicit commercial approval. Until then: **NO BUILD**.

PILOT_DELIVERY_READY
