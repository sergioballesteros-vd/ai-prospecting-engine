# Pilot stack matrix

Research cut-off: **2026-08-23**. Source IDs and official URLs are in [pilot_vendor_sources.md](./pilot_vendor_sources.md). “Public API not found” is not “API does not exist”; it means no implementation estimate may depend on it until the vendor supplies a contract.

## Existing-stack-first outcome

| Scenario | What to configure before any bridge | Residual bridge allowed only if… | Initial class |
|---|---|---|---|
| A — A3 + Microsoft 365 + Excel | A3/a3HRgo or a3innuva portal; A3 process alerts/tasks; dedicated shared mailbox/folder; approved Microsoft Form; Excel table in SharePoint/OneDrive; owner/cutoff views; Power Automate only if already licensed and acceptable. [WK-01–03, MS-10–11] | a validated cohort still cannot be tracked for completeness/owner/due date with the configured tools. | `CONFIGURE_EXISTING_STACK`; then Blueprint A. |
| B — A3 + Google Workspace + Sheets | A3 portal; dedicated address or Google Group Collaborative Inbox; Gmail labels/filters; approved Google Form linked to a protected Sheet. [WK-01–03, GG-07, GG-09–10] | form/portal adoption still leaves a measurable exception gap. | `CONFIGURE_EXISTING_STACK`; then Blueprint A. |
| C — Sage Despachos Connected + Microsoft 365 + Excel | Sage internal cases/tasks/request tracking, portal, labor alerts/comments, document management and Excel exports; Microsoft Form/shared mailbox only where Sage intake does not cover the cohort. [SG-01–07, MS-11] | the licensed Sage modules cannot expose a usable monthly-close view after vendor-supported configuration. | `CONFIGURE_EXISTING_STACK`; likely no custom bridge. |
| D — Bilky + email + portal | Bilky advisor/company/employee portals, custom forms/fields, tickets, alerts, document workflow, roles and import/export. [BL-01–05] | Bilky support confirms a specific missing status/reconciliation/report feature and a manual export cannot cover it. | `CONFIGURE_EXISTING_STACK`; highest risk that the “pilot” should be vendor configuration only. |
| E — Cegid/Diez + email + Excel/task system | DiezNOM portal, documents, communications and notifications; configure current task system/Excel for close exceptions. Validate whether another licensed Cegid module supplies request/validation workflow. [CG-01–04] | the exact Diez version/plan lacks required exception tracking and an approved export exists. | `CONFIGURE_EXISTING_STACK`; Blueprint A if gap remains. |
| F — Aplifisa + email + Excel/portal | Portal requests/incidents/status, Doc3W, email notices, labor Excel reports, profile permissions and support-assisted configuration. [AP-01–05] | native incidents/documents cannot represent the confirmed close checklist and the approved export/handoff is stable. | `CONFIGURE_EXISTING_STACK`; Blueprint A if gap remains. |

## Detailed product capability matrix

| Capability | A3 / WK | Sage Despachos Connected | Bilky | Cegid / Diez | Aplifisa |
|---|---|---|---|---|---|
| Relevant labor module | **CONFIRMED:** a3asesor Nom/a3innuva Nómina; portal may be a3HRgo/a3innuva Portal. [WK-01–03] | **CONFIRMED:** Laboral plus internal management and optional portals/document management. [SG-01–03] | **CONFIRMED:** HR, advisor/company/employee portals; not established as the payroll calculation system. [BL-01–03] | **CONFIRMED:** DiezNOM plus Portal del Empleado. [CG-01–02] | **CONFIRMED:** Gestión Laboral/Asesor Laboral, Portal del Empleado, Doc3W. [AP-01–04] |
| Client/employee collection | **CONFIRMED/PARTIAL:** employee data updates, requests, onboarding and variable concepts exist in cloud portal plans; confirm advisory-client workflow. [WK-02] | **CONFIRMED/PARTIAL:** portal requests and employee data/workflow are documented; exact Despachos plan/version unknown. [SG-03] | **CONFIRMED:** custom forms/fields, employee requests, tickets and connected portals. [BL-02–03] | **PARTIAL:** document sharing, messaging, vacations and notifications; exact monthly-close input form not documented. [CG-01–02] | **CONFIRMED/PARTIAL:** incidents, leave/vacation, personal data, documents and status; exact close form must be configured/validated. [AP-02, AP-04] |
| Document intake | **CONFIRMED:** portal document sharing/viewing; exact inbound types/limits unknown. [WK-01–03] | **CONFIRMED:** document management and portal publication; inbound client workflow depends on module. [SG-01, SG-07] | **CONFIRMED:** controlled upload/share, attachments, structured classification. PDF/JPG/PNG are explicitly listed for scanner, not necessarily every module. [BL-01–02] | **CONFIRMED/PARTIAL:** shared documentation in portal; Visualtime has request/upload/validation but cannot be attributed to DiezNOM without licensing confirmation. [CG-01, CG-03] | **CONFIRMED:** Doc3W bidirectional files, per-client disks and notifications. [AP-03] |
| Reminders/notifications | **CONFIRMED:** A3 task review/alerts and portal workflows; cadence/escalation details unknown. [WK-01] | **CONFIRMED:** labor alerts/comments and portal status; generic reminder cadence needs configuration. [SG-03, SG-06] | **CONFIRMED:** deadline alerts, internal/email notifications and tickets. [BL-02] | **CONFIRMED:** portal notifications; reminder rules/cadence unknown. [CG-01–02] | **CONFIRMED:** email notices and portal email notifications; exact cadence/configuration unknown. [AP-01, AP-02] |
| Tasks, owners, deadlines | **PARTIAL:** task review/process control; public pages do not specify an exception owner/deadline data model. [WK-01] | **CONFIRMED:** cases, tasks, workloads and real-time request tracking; likely closest native Sage fit. [SG-01–02] | **CONFIRMED:** pending tasks, assignees through tickets/processes, deadline alerts and CRM fields; validate exact modules. [BL-02, BL-05] | **PARTIAL:** messages/notifications are confirmed; generic tasks/owners/deadlines for DiezNOM are not. [CG-01–02] | **PARTIAL:** request state, incidents and communication exist; general owner/deadline model not publicly specified. [AP-02] |
| Exception/completeness tracking | **PARTIAL:** possible with portal request state plus A3 tasks, but no published “payroll close exception” object. | **PARTIAL:** tasks/requests/alerts can likely model it; validate configured fields and views. | **CONFIRMED/PARTIAL:** forms, fields, tickets, alerts and history can model a narrow queue; confirm rules and plan in demo. | **PARTIAL:** portal could collect/respond, but completeness queue not documented. | **PARTIAL:** incidents/request state can cover some cases; checklist completeness not documented. |
| Export/import/manual fallback | **CONFIRMED/PARTIAL:** reports exist; cloud API can read entities; exact legacy CSV/Excel formats need version-specific confirmation. [WK-01, WK-07] | **CONFIRMED:** many screens/reports export to Excel. [SG-03–05] | **CONFIRMED:** import/export is listed; exact schemas are unknown. [BL-02] | **NOT FOUND** in reviewed official Diez material; require vendor-supported export or Blueprint A with manual identifiers. | **CONFIRMED:** Excel economic reports, time-entry import and linked Aplifisa apps. [AP-01, AP-04] |
| Supported formats | **CONFIRMED/PARTIAL:** official cloud API is REST/JSON; portal supports labor documents, but public intake type/size limits were not found. [WK-02, WK-04] | **CONFIRMED:** payroll/certificates and document management include PDF/original office documents; portal/report exports include Excel. Exact import schemas are version-specific. [SG-03–05, SG-07] | **CONFIRMED/PARTIAL:** PDF/JPG/PNG are documented for scanner ingestion; document/ticket modules accept attachments, but their complete type/size allowlist is not public. [BL-02] | **UNKNOWN:** public portal pages confirm shared documents but do not publish type/size/export specifications. | **CONFIRMED/PARTIAL:** Excel labor reports and bidirectional Doc3W files; complete type/size/import specification is not public. [AP-03–04] |
| Public official API | **CONFIRMED only for named cloud products:** a3innuva Nómina REST API; not on-prem; Conectia required. [WK-04, WK-06] | **NOT FOUND for Despachos payroll.** Sage 200 APIs/partner ecosystem cannot be assumed to expose Despachos labor data. [SG-08–09] | **NOT FOUND.** Connectors are marketed, but no public contract. [BL-04] | **NOT FOUND** for DiezNOM. | **NOT FOUND** for Laboral/Portal. |
| Authentication/OAuth | **CONFIRMED:** WKA OAuth 2 Authorization Code, vendor-provisioned client, subscription key, tokens, TLS 1.2+. [WK-05] | **UNKNOWN for Despachos payroll.** Sage ID exists for Sage 200 API. [SG-09] | **UNKNOWN.** Portal roles exist; API auth not public. | **UNKNOWN.** Portal auth/API auth not publicly specified. | **UNKNOWN.** user/password portal access is implied; API auth absent. |
| Least-privilege/read-only | **PARTIAL:** restricted WKA task/company/site/employee access exists; code can issue GET only, but official changelog says read/write permissions are not separated. [WK-06, WK-08] | **UNKNOWN** for API. Use exported files or user-level read-only UI/report rights where vendor supports them. | **PARTIAL:** roles/access controls confirmed; no API read-only claim. [BL-01–02] | **UNKNOWN.** | **UNKNOWN/PARTIAL:** distinct profiles exist, but fine-grained API/read-only permissions not public. [AP-02] |
| Webhooks | **NOT FOUND for payroll.** Accounting webhooks are not evidence for Nómina. | **NOT FOUND** for Despachos payroll. | **NOT FOUND.** | **NOT FOUND.** | **NOT FOUND.** |
| API limitations/rate evidence | **CONFIRMED/PARTIAL:** lists can be limited to 50 records/page; access tokens default to 60 minutes and refresh tokens 30 days. A payroll-specific public rate-limit page was not found. [WK-05, WK-09] | **UNKNOWN for Despachos payroll.** Do not borrow Sage 200/Accounting quotas. | **UNKNOWN:** no public API contract/limits. | **UNKNOWN:** no public API contract/limits. | **UNKNOWN:** no public API contract/limits. |
| Safe write-back | **NOT RECOMMENDED:** API exposes high-impact payroll writes and does not separate read/write permission; no generic safe task/note endpoint found. [WK-07–08] | **NOT FOUND:** no official bounded API operation established. | **NOT FOUND:** use native UI/configuration, not custom write. | **NOT FOUND.** | **NOT FOUND.** |
| Licensing/plan dependency | **CONFIRMED:** portal has plans/modules; API requires Conectia and a cloud product. [WK-02, WK-04, WK-06] | **CONFIRMED/PARTIAL:** modular; exact portal/management/Power Automate entitlements are customer-specific. [SG-01–03] | **CONFIRMED:** public Basic/Premium plan distinctions; validate workflow/module entitlement. [BL-01] | **UNKNOWN:** confirm Diez/portal modules and any Visualtime dependency. | **CONFIRMED/PARTIAL:** separate portal/Doc3W services are marketed; current contract unknown. [AP-01–03] |
| Integration/partner ecosystem | **CONFIRMED:** Conectia APIs, a3Marketplace/certified apps and a partner network are public; exact payroll connector scope still requires product evidence. [WK-10] | **CONFIRMED:** Sage Tech Partner marketplace includes Sage 200/Despachos ecosystem; it does not prove payroll API semantics. [SG-08] | **CONFIRMED:** Bilky lists 47 accounting integrations including named A3/Sage/Cegid/Aplifisa products; protocols and payroll objects are not public. [BL-04] | **PARTIAL:** Cegid support/commercial channel is official; Diez developer/partner contract was not found. [CG-04] | **CONFIRMED/PARTIAL:** linked Aplifisa applications and dedicated labor support exist; external developer ecosystem/API not found. [AP-04–05] |
| Preferred implementer | WK/authorized partner for portal/Conectia/OAuth; Sergio only for residual metadata bridge. | Sage/Tech Partner for module activation/export/API; Sergio only after a documented gap. | Bilky support for configuration/connectors; likely no custom code. | Cegid/Diez support for portal/export; Sergio only with stable manual handoff. | Aplifisa labor support for portal/Doc3W/exports; Sergio only for residual queue. |

## Email layer: minimum-invasive choices

### Microsoft 365

1. **First choice — no API:** a dedicated corporate shared mailbox or dedicated folder, approved Outlook rules, a Microsoft Form for structured submissions, and an Excel table in SharePoint/OneDrive. Humans own replies. [MS-11]
2. **Second choice — existing Power Automate:** shared-mailbox trigger → deduplicate by immutable message ID → create/update metadata row → draft/manual reminder queue. Treat triggers as hints because Microsoft documents missed/duplicate/attachment edge cases. [MS-10]
3. **Custom Graph only after residual gap:**
   - Prefer delegated access for one named operator and only the mailbox they already access. `Mail.ReadBasic` is insufficient if parsing body/attachments; use `Mail.Read`/`Mail.Read.Shared` only if required. [MS-01–03]
   - For unattended access to a shared mailbox subscription, app-only `Mail.Read` is required; constrain it with Exchange App RBAC to the single pilot mailbox. [MS-02, MS-04, MS-06]
   - Subscribe to the dedicated folder, validate `clientState`, renew before expiry, and use folder delta queries as reconciliation. [MS-05–08]
   - Do not request `Mail.ReadWrite` or `Mail.Send` for Blueprint A. Fetch an attachment only after an allowlist/size/type check and only if metadata is insufficient. [MS-09]
   - Align mailbox and copied-metadata retention. A copy in Postgres/Excel is a separate record and does not inherit Purview behavior. [MS-12]

**Least-invasive pilot architecture:** shared mailbox + folder + customer-managed form/Excel. Graph is conditional. A personal mailbox is rejected.

### Google Workspace

1. **First choice — no API:** Google Group Collaborative Inbox for assignment/completion, or a dedicated delegated account if true Gmail behavior is needed; approved Google Form → Sheet; Gmail labels/filters for a dedicated route. [GG-07–10]
2. **Apps Script only if customer accepts it:** form-submit/time-driven trigger under a named customer-owned automation account. It is configuration/custom scripting, must have an owner/offboarding plan, and must not send free-form replies.
3. **Custom Gmail API only after residual gap:**
   - Use user OAuth to one dedicated mailbox. Avoid domain-wide delegation. Google explicitly recommends avoiding it when OAuth consent works. [GG-06]
   - `gmail.metadata` can support routing by headers/labels but cannot read body/attachments; `gmail.readonly` is necessary for content and is a restricted scope with verification/security-assessment implications when data is stored/transmitted server-side. [GG-01]
   - A label-filtered `watch` reduces event noise but uses Pub/Sub, must be renewed at least every seven days, and must reconcile using `history.list`; a stale history ID requires full sync. [GG-03–04]
   - Attachment retrieval requires broad read scope; default to not downloading. [GG-05]
   - Mailbox delegation is mailbox-wide, not label-scoped. Prefer a dedicated pilot mailbox rather than granting access to an operational inbox. [GG-08]
   - Align Vault and pilot-store retention explicitly. [GG-11]

**Least-invasive pilot architecture:** Collaborative Inbox or dedicated mailbox + form/Sheet. Gmail API and Pub/Sub are conditional and normally too much for a €1,000 setup.

## No-API fallback playbook

| System | Fallback order | RPA decision |
|---|---|---|
| A3 legacy/on-prem or no Conectia | 1) activate a3HRgo/a3innuva portal if compatible; 2) A3 task/alert configuration; 3) existing report/manual export; 4) Outlook/Gmail + Excel/Sheet queue keyed by A3 company code; 5) vendor/partner-supported integration; 6) no integration. | **REJECTED** for payroll writes. **LAST_RESORT** only for a read-only export if vendor approves it in writing, no supported export exists, test environment is available, and the pilot price/scope is reworked. |
| Sage Despachos Connected | 1) internal cases/tasks/request tracking; 2) portal/labor alerts/document module; 3) supported Excel export; 4) mailbox/form queue; 5) Sage Tech Partner; 6) no integration. | **REJECTED** by default; UI/version changes and payroll impact make browser automation disproportionate. |
| Bilky | 1) configure forms/fields/tickets/alerts/roles; 2) use native import/export; 3) ask Bilky to configure an existing connector; 4) metadata queue outside Bilky; 5) no integration. | **REJECTED.** A native configurable portal exists; automate its UI only if Bilky itself provides/sponsors the method, which then becomes vendor-supported, not Sergio’s brittle RPA. |
| Cegid/Diez | 1) portal/notifications; 2) current task system/Excel keyed by Diez company ID; 3) supported report/export confirmed by support; 4) Cegid partner; 5) no integration. | **REJECTED** by default; **LAST_RESORT** read-only export only under the same written/vendor/test restrictions. |
| Aplifisa | 1) Portal incidents/status; 2) Doc3W; 3) email notice module; 4) Excel report; 5) Aplifisa support; 6) external metadata queue/no integration. | **REJECTED** by default because supported portal, Excel and vendor help paths exist. |

Never read vendor databases directly, scrape internal pages, replay private network calls, or import a file into payroll without vendor documentation and human validation.

## Delivery estimates by blueprint and stack

Hours are one engineer, one workflow/cohort/close, prepared client, metadata only. `R/S` = research/setup, `Cfg` = configuration, `Impl` = implementation, `Coord` = client/vendor coordination, `Test`, `Train`, `M1` = first-month support, `Maint` = recurring hours/month. Ranges are estimates, not vendor commitments.

| Stack | Blueprint | R/S | Cfg | Impl | Coord | Test | Train | M1 | Maint | Fit / major uncertainty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A3 + M365 | A | 3–6 | 5–10 | 0–12 | 3–6 | 5–8 | 2–4 | 3–6 | 1–3 | **GOOD FIT** if Forms/Excel/shared mailbox suffice; Power Automate licensing and A3 version unknown. |
| A3 + Google | A | 3–6 | 5–10 | 0–10 | 3–6 | 5–8 | 2–4 | 3–6 | 1–3 | **GOOD FIT** if Form/Sheet/Group suffices; Gmail restricted scopes would make it conditional. |
| Sage + M365 | A | 4–8 | 6–12 | 0–8 | 4–8 | 5–8 | 2–4 | 3–6 | 1–3 | **GOOD FIT** when native tasks/portal/export are licensed; vendor configuration may dominate. |
| Bilky | A | 3–6 | 6–12 | 0–4 | 3–6 | 4–8 | 2–4 | 2–5 | 1–2 | **GOOD FIT for configuration**, but existing stack may eliminate custom recurring service. |
| Cegid/Diez | A | 4–8 | 4–10 | 0–10 | 5–10 | 5–8 | 2–4 | 3–6 | 1–3 | **CONDITIONAL:** public export/task detail is weak; must not wait on an undocumented API. |
| Aplifisa | A | 3–7 | 5–10 | 0–8 | 4–8 | 5–8 | 2–4 | 3–6 | 1–3 | **GOOD FIT/CONDITIONAL:** portal/Doc3W/Excel credible; exact plan and queue semantics unknown. |
| a3innuva cloud | B | 8–14 | 3–6 | 16–30 | 6–12 | 10–16 | 2–4 | 6–10 | 3–6 | **CONDITIONAL:** 45–82 total hours, Conectia/client OAuth and non-separated read/write permission. Usually outside €1,000 setup. |
| A3 legacy/on-prem | B | 5–10 | 2–6 | 8–16 | 4–8 | 6–10 | 2–4 | 4–8 | 2–4 | **CONDITIONAL** only as scheduled supported export, not an API. |
| Sage | B | 6–12 | 2–6 | 8–18 | 6–14 | 8–12 | 2–4 | 5–8 | 2–5 | **BAD FIT until vendor supplies an official payroll API/export contract.** Export-only reconciliation can be re-scoped. |
| Bilky | B | 6–12 | 2–5 | 8–18 | 6–12 | 8–12 | 2–4 | 4–8 | 2–5 | **BAD FIT** unless Bilky supplies a supported API/connector; native config is better. |
| Cegid/Diez | B | 6–12 | 2–6 | 8–18 | 8–16 | 8–12 | 2–4 | 5–8 | 2–5 | **BAD FIT** until official read interface/export is confirmed. |
| Aplifisa | B | 6–10 | 2–6 | 8–16 | 6–12 | 8–12 | 2–4 | 4–8 | 2–5 | **BAD FIT** for API; **CONDITIONAL** for a stable supported Excel export. |
| Any stack | C | 10–20 | 4–8 | 24–60 | 8–20 | 16–30 | 3–6 | 8–16 | 5–10 | **BAD FIT.** No reviewed vendor exposes a proven safe bounded task/note write for this pilot; `NO_SAFE_WRITEBACK_RECOMMENDED`. |

### €1,000 setup conclusion

- **Compatible:** Blueprint A when total delivery is held to roughly **18–35 hours**, access is ready, native tools are used, and support is bounded.
- **Conditional:** Blueprint A at 35–45 hours only as a deliberate design-partner subsidy with reusable learning; it is not a repeatable unit-economics baseline.
- **Not compatible:** new OAuth/API approval, restricted-scope verification, unknown vendor APIs, RPA, custom document processing, or Blueprint C. Blueprint B should be a separately priced change order after evidence that it materially improves the metric.

## Strict blueprint × scenario estimate grid

This grid makes the six requested environments explicit. Hours are ranges for one engineer. `R/S` = research/setup, `Cfg` = configuration, `Impl` = implementation, `Coord` = client/vendor coordination, `Test`, `Train`, `M1` = first-month support, and `Maint` = recurring hours/month. Overlapping work is possible, so columns must not be treated as a precise invoice sum.

| Scenario | Blueprint | R/S | Cfg | Impl | Coord | Test | Train | M1 | Maint | Classification and major uncertainty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A — A3 + M365 + Excel | A | 3–6 | 5–10 | 0–12 | 3–6 | 5–8 | 2–4 | 3–6 | 1–3 | **GOOD FIT:** exact A3/portal plan and Power Automate entitlement. |
| B — A3 + Gmail + Sheets | A | 3–6 | 5–10 | 0–10 | 3–6 | 5–8 | 2–4 | 3–6 | 1–3 | **GOOD FIT:** Group/delegated mailbox and Form/Sheet ownership. |
| C — Sage + M365 + Excel | A | 4–8 | 6–12 | 0–8 | 4–8 | 5–8 | 2–4 | 3–6 | 1–3 | **GOOD FIT:** licensed Sage tasks/portal/export may solve all. |
| D — Bilky + email + portal | A | 3–6 | 6–12 | 0–4 | 3–6 | 4–8 | 2–4 | 2–5 | 1–2 | **GOOD FIT for configuration:** custom recurring value may disappear. |
| E — Cegid/Diez + email + Excel/task | A | 4–8 | 4–10 | 0–10 | 5–10 | 5–8 | 2–4 | 3–6 | 1–3 | **CONDITIONAL:** exact export/task capability needs support confirmation. |
| F — Aplifisa + email + Excel/portal | A | 3–7 | 5–10 | 0–8 | 4–8 | 5–8 | 2–4 | 3–6 | 1–3 | **GOOD FIT/CONDITIONAL:** exact portal/Doc3W plan and checklist semantics. |
| A — A3 + M365 + Excel | B | 8–14 | 3–6 | 16–30 | 6–12 | 10–16 | 2–4 | 6–10 | 3–6 | **CONDITIONAL:** only cloud a3innuva+Conectia; WKA/OAuth and no read/write separation. Legacy requires B-lite export. |
| B — A3 + Gmail + Sheets | B | 8–14 | 3–6 | 18–34 | 6–12 | 10–16 | 2–4 | 6–10 | 3–6 | **CONDITIONAL/BAD AT €1,000:** same ERP constraints plus Gmail restricted-scope/Pub/Sub overhead if email API is also needed. |
| C — Sage + M365 + Excel | B | 6–12 | 2–6 | 8–18 | 6–14 | 8–12 | 2–4 | 5–8 | 2–5 | **BAD FIT** until official payroll interface; **CONDITIONAL** as stable supported Excel export only. |
| D — Bilky + email + portal | B | 6–12 | 2–5 | 8–18 | 6–12 | 8–12 | 2–4 | 4–8 | 2–5 | **BAD FIT:** no public API contract; native configuration should win. |
| E — Cegid/Diez + email + Excel/task | B | 6–12 | 2–6 | 8–18 | 8–16 | 8–12 | 2–4 | 5–8 | 2–5 | **BAD FIT:** public read/export contract not established. |
| F — Aplifisa + email + Excel/portal | B | 6–10 | 2–6 | 8–16 | 6–12 | 8–12 | 2–4 | 4–8 | 2–5 | **BAD FIT for API; CONDITIONAL for supported Excel export.** |
| A — A3 + M365 + Excel | C | 10–20 | 4–8 | 24–60 | 8–20 | 16–30 | 3–6 | 8–16 | 5–10 | **BAD FIT:** A3 exposes high-impact writes and no read/write permission separation; no safe task/note write found. |
| B — A3 + Gmail + Sheets | C | 10–20 | 4–8 | 24–60 | 8–20 | 16–30 | 3–6 | 8–16 | 5–10 | **BAD FIT:** same ERP risk; email platform does not reduce it. |
| C — Sage + M365 + Excel | C | 10–20 | 4–8 | 24–60 | 8–20 | 16–30 | 3–6 | 8–16 | 5–10 | **BAD FIT:** no official bounded Despachos payroll task/note write contract found. |
| D — Bilky + email + portal | C | 8–16 | 4–8 | 20–50 | 8–18 | 14–26 | 3–6 | 8–14 | 4–8 | **BAD FIT:** use Bilky native UI/support; no public API/write/rollback contract. |
| E — Cegid/Diez + email + Excel/task | C | 10–20 | 4–8 | 24–60 | 10–22 | 16–30 | 3–6 | 8–16 | 5–10 | **BAD FIT:** public bounded write/auth/audit/reversal evidence absent. |
| F — Aplifisa + email + Excel/portal | C | 10–18 | 4–8 | 22–55 | 8–20 | 14–28 | 3–6 | 8–16 | 5–10 | **BAD FIT:** use portal/UI; public bounded write/auth/rollback contract absent. |

All Blueprint C rows resolve to `NO_SAFE_WRITEBACK_RECOMMENDED`; the ranges show why they are economically incompatible, not an invitation to estimate/build them.
