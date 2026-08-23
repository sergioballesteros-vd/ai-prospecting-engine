# Pilot economic kill criteria

The offer hypothesis is €1,000 setup + €200/month. The setup is viable only as a **narrow configuration-led pilot**, ideally about 18–35 total delivery hours and no more than 3–7 working days elapsed effort for one engineer. These are capacity boundaries, not an hourly-rate claim.

## Pre-acceptance kill gates

Reject or re-scope before signature if any is true:

| Kill fact | Decision | Why it breaks the offer |
|---|---|---|
| More than one payroll system, workflow, cohort or monthly close | `REJECT_OR_SPLIT` | Testing/mapping/support multiply and the outcome becomes ambiguous. |
| Payroll calculation, salary/employee/legal field mutation, government filing or autonomous labor/legal decision expected | `REJECT` | Outside product/safety boundary and liability is disproportionate. |
| Custom connector is required before native portal/task/export configuration is tried | `CONFIGURE_EXISTING_STACK` | The buyer already pays for the lower-risk path. |
| Existing licensed tool can solve it cheaply | `RECOMMEND_EXISTING_TOOL` | Building creates duplicate cost and maintenance without residual value. |
| API access requires long certification, partner status, new module procurement or vendor approval on critical path | `RE_SCOPE_OR_REPRICE` | Timeline and cost are not controllable inside €1,000. |
| No official API/export contract; proposal relies on reverse engineering, direct DB access, private APIs or RPA | `REJECT` | Brittle, unsafe and likely to fail vendor terms/updates. |
| Broad mailbox/domain access, shared passwords, personal inbox/WhatsApp or non-revocable credentials required | `REJECT` | Least privilege and offboarding cannot be met. |
| Customer expects document archive/OCR/general email classifier | `REJECT_OR_NEW_PROJECT` | Adds sensitive data, error surface and product scope. |
| Sensitive/special-category/payroll documents are unavoidable but security/legal review is not complete | `REJECT_PENDING_REVIEW` | Data obligations exceed the default pilot and cannot be priced blindly. |
| Workflow cannot be isolated or manual fallback cannot operate | `REJECT` | Fail-closed operation would threaten the monthly close. |
| No sponsor, operator, reviewer, backup or client implementation owner | `REJECT` | Sergio would become the operational owner/general IT desk. |
| No usable baseline, cutoff, target or measurement method | `MEASURE_FIRST` | No credible proof of value or renewal decision. |
| Buyer refuses rehearsal, human approval, audit, access control, retention/deletion or kill criteria | `REJECT` | Safety and learning loop are not enforceable. |
| Buyer expects autonomous messages, unlimited changes, SLA/on-call or general IT support | `REJECT_OR_ENTERPRISE_REPRICE` | €200/month cannot sustain the obligation. |
| Expected build exceeds roughly 35–45 hours at the setup price | `CHANGE_ORDER_OR_STOP` | The first case becomes an unbounded subsidized integration. |
| Expected recurring work exceeds a small monthly review/support envelope | `REPRICE_OR_STOP` | Maintenance consumes the monthly fee and founder capacity. |
| Only value is “AI” without a measurable operational exception problem | `REJECT` | There is no outcome to buy or validate. |

## Economics by blueprint

| Blueprint | Likely total | €1,000 setup | €200/month | Economic decision |
|---|---:|---|---|---|
| A0 — customer-owned configuration | 18–30 hours | Compatible if access/content are ready and configuration is reusable | Compatible for bounded close review, health/status report and small rule/template maintenance | **GOOD FIT** |
| A1 — tiny metadata bridge | 25–45 hours | Compatible only at low end or as an explicit design-partner subsidy | Conditional on stable, low-touch operation and no mailbox/vendor churn | **CONDITIONAL** |
| B-lite — supported CSV/Excel export | 28–45 hours | Conditional; estimate schema stability and manual owner | Conditional; export failures/reconciliation must stay bounded | **CONDITIONAL** |
| B — official API | 45–82+ hours for documented a3 cloud case; unknown elsewhere | Not compatible without separate integration fee | €200 may not cover token/vendor/API maintenance and support | **BAD FIT at current setup price** |
| C — write-back | 65–134+ hours plus security/vendor coordination | Not compatible | Not compatible with required assurance/support | **BAD FIT / NO SAFE WRITEBACK** |

The first setup fee should pay for a repeatable operational intervention, not fund discovery of an undocumented vendor interface. A design-partner discount is valid only when its maximum subsidy, reusable learning and stop date are explicit.

## Monthly maintenance budget test

Before accepting €200/month, define exactly:

- One close-health/status review and short outcome report.
- Monitoring/alert review during an agreed close window.
- A small fixed amount of rule/template correction, not new categories/workflows.
- Incident triage for Sergio’s component, not customer IT/vendor support.
- No response-time guarantee beyond the agreed window unless separately priced.

Kill or reprice recurring service if any two months show:

- Repeated manual data repair or source-to-queue reconciliation.
- Vendor/API/schema breakage or OAuth reauthorization requiring substantial work.
- More than the agreed support/change allowance.
- Customer asks Sergio to operate the queue or chase its clients.
- False/incorrect reminders require frequent intervention.
- No adoption or measurable improvement.
- Hosting/tool/subprocessor cost plus support consumes most of the fee.

## When Sergio should recommend a third-party tool instead

This is a successful commercial outcome when it protects trust and founder capacity.

Recommend the existing vendor/partner or a third-party tool when:

1. **Native fit:** Bilky forms/tickets/alerts, Sage tasks/portal, A3 portal, Cegid portal or Aplifisa portal/Doc3W already covers intake, owner, status and reminders.
2. **Certified integration required:** the customer needs a supported payroll connector, SLA, sandbox, vendor certification or broad product coverage Sergio cannot economically provide.
3. **Multi-system requirement:** the buyer needs a universal payroll hub, multi-ERP workflow, SSO/governance across many clients, or enterprise audit/retention.
4. **Communication platform requirement:** the buyer needs production omnichannel/WhatsApp Business, consent/opt-out, high availability and regulated message operations.
5. **Document automation requirement:** the core problem is high-volume OCR/document capture with established accuracy, review and archival requirements.
6. **Security/compliance requirement:** certifications, dedicated security team, 24/7 incident response, customer-managed keys, complex residency or procurement exceed current capability.
7. **Economics:** implementation/maintenance cannot fit the price and a mature product costs less than custom support.

Sergio may charge for discovery, vendor selection, configuration, migration and measurement if transparently scoped. He should not disguise vendor configuration as proprietary software or create a bridge merely to preserve the sale.

## What not to build

| Rejected build | Why premature |
|---|---|
| Universal A3 connector | “A3” spans legacy/on-prem and cloud products; cloud API needs Conectia/vendor OAuth and exposes broad payroll writes. One customer’s mapping is not a universal contract. |
| Universal Sage connector | Public Despachos payroll API evidence is absent; Sage products/APIs are not interchangeable. |
| Universal payroll abstraction | Hides product/version/legal semantics before one workflow proves repeatability; multiplies test and liability surface. |
| Multi-tenant SaaS | One customer has not proven repeated demand; isolation, tenancy, billing, identity and support would consume the pilot economics. |
| OCR engine | Default should not ingest documents; mature tools exist and accuracy/security review exceeds the one-workflow need. |
| General email classifier | The approved route/checklist is narrow; general mailbox access and open-ended labels expand privacy/error risk. |
| Chatbot | No validated conversational job; it encourages unreviewed advice and scope creep. |
| Generic workflow builder | Native portals/tasks already exist; configurable product infrastructure is not needed for one close. |
| WhatsApp automation platform | Personal WhatsApp is prohibited; official Business setup, consent, retention, DPA and operations are a separate product. |
| Payroll engine | Explicitly out of scope, regulated/high-impact and duplicates the system of record. |
| Legal decision agent | LLM/rules must not decide employment status, agreements, legal sufficiency or filing. |
| Customer-facing mobile app | Portals/mobile apps already exist; no validated distribution or workflow need. |
| Full CRM | Queue is one monthly-close workflow, not sales/contact management. |
| Custom portal | Existing payroll/customer/employee portals and forms must be configured first; build only after a paid case proves an irreducible need. |
| Browser automation/RPA | Fragile UI dependency, hard to test/audit, broad credentials and dangerous payroll mutation risk. |
| Event bus/Redis/Celery/microservices | One customer/close does not justify distributed operations; a customer-owned file or one scheduled job is enough. |
| LLM pipeline by default | Deterministic checklist and human review can operate without it; it adds sensitive-data, cost and uncertainty controls. |

## Acceptance rule

Accept only when all are true:

- Native-stack test leaves a specific residual gap.
- Blueprint A can solve it without ERP write and with metadata only.
- Total setup effort and first-month support fit the price/capacity.
- Customer provides owner, access, baseline, rehearsal and human review.
- Security/privacy obligations are approved and operationally achievable.
- Manual fallback and offboarding are real.

Otherwise recommend configuration/third party, run `MEASURE_FIRST`, re-scope/reprice, or decline.
