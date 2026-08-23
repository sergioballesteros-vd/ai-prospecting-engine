# Pilot stack recommendation

## One clear default

**Default: Blueprint A0 — configure the customer’s existing stack, with no ERP integration and no custom hosted service unless a measured residual gap remains.**

- Approved corporate form/portal or dedicated routed mailbox.
- Metadata-only exception queue in the customer’s Excel/SharePoint, Google Sheet, or native task/portal tool.
- Deterministic, versioned completeness checklist.
- Named owner, due date, next action and bounded reminder review list.
- Firm-approved templates; the firm owns and sends communication.
- Human review before `APPROVED` and manual handoff to payroll.
- No payroll calculation, filing, legal decision, document archive, personal WhatsApp, or ERP write.
- LLM disabled by default.

This is deliverable by one engineer in approximately **3–7 working days** when the `pilot_candidate_handoff` is complete, access is ready, and delivery stays around **18–35 hours**. A €1,000 setup is commercially compatible only within that boundary. The €200/month must buy a bounded service—health/status review, exception metrics, one monthly close review and small agreed rule/template maintenance—not unlimited support.

## Pre-build decision ladder

1. **Can the licensed payroll portal/task system already collect, assign, remind and show status?** Configure it with the vendor/partner. Outcome: `CONFIGURE_EXISTING_STACK`.
2. **Can a customer-owned Form + Excel/Sheet + shared/collaborative inbox close the gap?** Configure A0. No custom code.
3. **Is one small residual behavior missing after a rehearsal?** Add A1, a single-client metadata bridge with no ERP access.
4. **Does read-only reconciliation remove a measured, recurring failure and is a supported interface already available?** Consider B or B-lite export.
5. **Is a bounded non-payroll write separately permissioned and officially documented?** None was found in current research. Keep manual handoff: `NO_SAFE_WRITEBACK_RECOMMENDED`.

## Upgrade facts: A → B → C

### A0 → A1 (tiny metadata bridge)

All must be true:

- A real monthly close rehearsal proves the native configuration cannot produce the required owner/completeness/cutoff view.
- The residual behavior is narrow, deterministic and reusable for the one cohort.
- A dedicated corporate input route is available.
- Metadata-only storage is sufficient.
- Client accepts single-customer deployment, DPA, retention, access and incident plan.
- Estimated implementation remains within the commercial cap or a change order is approved.

### A/A1 → B (read-only ERP reconciliation)

All must be true:

- Baseline shows a recurring reconciliation failure with material time/error consequence.
- Official API or stable vendor-supported export exposes the exact minimum fields.
- Customer has the needed product/version/module/plan and vendor approval is not on the critical path.
- Authentication, least-privilege scope, audit, rate limit and fallback are documented.
- A verified exact mapping exists; no fuzzy employee matching.
- Benefit exceeds access, build, testing and maintenance cost.
- Blueprint A remains a tested fallback.

Current evidence supports API B only for **cloud a3innuva Nómina + Conectia**, and even there it is conditional because WK documents no read/write permission separation. A stable supported export may enable B-lite elsewhere.

### B → C (limited write-back)

Required facts are stricter: an official endpoint for one non-payroll task/note/state, separately scoped write permission, test tenant, idempotency, read-after-write verification, immutable audit, written client approval and documented reversal/compensation. No reviewed vendor meets this evidence threshold. Therefore C is not a first-pilot option.

## Easiest first-case stack ranking

Ranking is for **safe monthly-close exception delivery using verified native configuration/export evidence**, not generic product quality or market share.

1. **Bilky** — native advisor/company/employee portals, configurable fields/forms, tickets, deadline alerts, attachments, history, roles, email notifications and import/export are closest to the required queue. The likely correct outcome is configuration, not custom software. [Official functionality](https://bilky.es/funcionalidades/)
2. **Sage Despachos Connected** — internal tasks/cases/workloads/request tracking, portal, labor alerts/comments and documented Excel export are strong. Exact licensed modules/version remain a gate. [Official product](https://www.sage.com/es-es/software-asesorias-y-despachos/)
3. **Aplifisa** — Portal incidents/request status, Doc3W, email notices and labor Excel exports give credible no-API paths; public task-owner/deadline semantics are less clear. [Official labor product](https://www.aplifisa.com/asesorias/programa-laboral-aplifisa/)
4. **A3 / Wolters Kluwer** — strong portal and the only verified public cloud payroll API, but the generic “A3” label hides a decisive cloud-vs-on-prem split, Conectia/vendor OAuth dependencies, and non-separated read/write API permissions. It rises to first for a **separately priced read-only B** when the exact stack is cloud a3innuva Nómina + Conectia. [Official API prerequisites](https://a3developers.wolterskluwer.es/doc/a3innuva-n%C3%B3mina/como-empezar/)
5. **Cegid/Diez** — portal, documents, messages, vacations and notifications are verified, but public Diez export/task/API detail is the weakest of the five for estimating a residual bridge. [Official portal](https://www.cegid.com/ib/es/productos/software-programa-erp-asesorias-gestorias/portal-empleado/)

The ranking must be recomputed after discovery. A configured portal can make a prospect easier technically but commercially ineligible because `EXISTING_STACK_SOLVES_IT`.

## Platform recommendation when A1 is justified

1. Reuse the project’s FastAPI/SQLAlchemy/Postgres engineering conventions, not its production data store or in-process research runner.
2. Deploy one customer in a separate small service and separate paid Postgres in Render Frankfurt; no multi-tenancy, Redis, Celery or general workflow builder.
3. Use one scheduled reconciliation job, idempotency, health endpoint, structured metadata-only logs, paid backups and a tested manual fallback.
4. Authenticate operators through a customer-approved identity path; the Prospecting Engine’s coarse `APP_API_TOKEN` pattern is not an adequate final control for employee/payroll-adjacent access.
5. Keep the Prospecting Engine and pilot operational data separated. This avoids expanding an internal sales/research system into a payroll-data processor by accident.

If customer-owned M365/Google configuration is sufficient, do not deploy anything.

## Go/no-go summary

| Question | Decision |
|---|---|
| Can the first pilot avoid payroll-system writes? | **YES.** It should. |
| Can the default pilot fit 3–7 working days? | **DEPENDS:** yes with complete handoff, ready access and metadata-only A0/small A1; otherwise re-scope. |
| Is €1,000 setup compatible? | **CONDITIONAL:** good at 18–35 hours; re-scope/reprice beyond roughly 35–45 hours. |
| Is an LLM needed? | **NO.** Add only after deterministic failure is measured. |
| Is ERP read access needed? | **NO by default.** It is a separately justified upgrade. |
| Is any ERP write recommended? | **NO.** `NO_SAFE_WRITEBACK_RECOMMENDED`. |

## Exact refusal facts

Refuse or re-scope if discovery establishes any of the following:

- More than one payroll product, workflow, cohort or close is required.
- The buyer expects salary calculation, legal/labor interpretation, employment-status decisions, filing or automatic payroll mutation.
- Personal WhatsApp, shared passwords, production database access, browser scraping/RPA, or unrestricted mailbox/domain access is required.
- There is no sponsor, workflow owner, cutoff, cohort, baseline, measurable outcome or human approval point.
- Existing licensed configuration can solve the problem at lower risk/cost and the buyer will not use it.
- Required data includes salary/bank/ID/health/union/garnishment/leave-detail documents without completed security review, lawful basis, DPA, controls and economically viable scope.
- The customer refuses data minimization, access revocation, retention/deletion, incident responsibilities, test-data discipline, audit or a manual fallback.
- API/export access is undocumented, depends on long certification/partner approval, cannot be least-privilege, or lacks a stable test path.
- Delivery is expected to exceed roughly 35–45 hours at €1,000 without an approved change order.
- Expected recurring maintenance/support exceeds what €200/month can cover, or the buyer expects general IT support/unlimited changes.
- The workflow cannot fail closed when information is incomplete, contradictory or stale.
- The customer will not rehearse, train operators, measure the baseline or honor kill criteria.

## Stop condition

This recommendation does not authorize implementation. The next technical action requires all three:

1. `PILOT_CANDIDATE`
2. completed `pilot_candidate_handoff`
3. Sergio’s explicit commercial approval

Until then: **NO BUILD**.
