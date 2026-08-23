# First-pilot privacy and security checklist

Recommended default: **store metadata and status, not payroll documents, unless the validated pilot requires them.** This is an engineering checklist, not legal advice. The customer’s privacy lead/DPO or counsel decides lawful basis, notices, role allocation, DPIA need and contractual language.

Official anchors: [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [EDPB controller/processor guidance](https://www.edpb.europa.eu/documents/guideline/guidelines-072020-on-the-concepts-controller-and-processor-in-the-gdpr_en), [AEPD security guidance](https://www.aepd.es/derechos-y-deberes/cumple-tus-deberes/medidas-de-cumplimiento/seguridad-de-los-tratamientos), and [AEPD risk/DPIA guide](https://www.aepd.es/guias/gestion-riesgo-y-evaluacion-impacto-en-tratamientos-datos-personales.pdf).

## Hard gate before access

- [ ] Customer legal entity, sponsor, workflow owner, privacy/security owner and Sergio’s entity are recorded.
- [ ] Roles are determined from actual purposes/means. Expected default: advisory firm/customer is controller; Sergio is processor for the bounded pilot. Confirm whether end-client companies create joint/separate-controller complexity.
- [ ] Article 28-compliant DPA is signed before production data access; instructions, confidentiality, security, subprocessors, assistance, breach notice, deletion/return and audit terms are included.
- [ ] Lawful basis, transparency/employee notices and any labor-law consultation obligations are confirmed by the controller.
- [ ] Processing record/data-flow diagram names each system, data category, actor, location, transfer and retention period.
- [ ] Risk assessment is completed; DPIA need is assessed before any high-risk processing. High residual risk stops the pilot.
- [ ] One client, cohort, close, approved channels and prohibited fields are contractually scoped.

## Data inventory and minimization

- [ ] Queue schema is limited to company reference/name, period, controlled status/exception/missing-item codes, owner, next action, due/contact timestamps, source opaque IDs and audit events.
- [ ] Company/employee identifiers are pseudonymous or customer-owned internal references where possible.
- [ ] Free text is minimized; controlled codes are preferred.
- [ ] Email bodies are processed transiently only if the approved form/subject metadata is insufficient.
- [ ] Attachments are not downloaded or retained by default. Store filename/type/size/provider ID and review result, not bytes.
- [ ] Payroll PDFs and source documents remain in the customer’s existing portal/mailbox/document system.
- [ ] No salary, bank account, tax identifier, national ID, Social Security number, address, dependants, garnishment, union membership, health/IT details, biometric/geolocation, collective-agreement interpretation or payroll calculation is stored.
- [ ] No full mailbox sync, contact enrichment or non-cohort records.
- [ ] No production content is copied into prompts, tickets, analytics, screenshots or developer tools.

## Security-review triggers

Stop and obtain a documented security/privacy decision before processing:

- Health, disability, medical certificate, sickness/IT reason or other Article 9 special-category data.
- Union membership or data revealing racial/ethnic origin, beliefs, sex life/orientation, genetics or biometrics.
- Salary, bank details, garnishments, tax/benefit/dependant data, national identifiers or Social Security numbers.
- Payroll documents, employment contracts, disciplinary files, legal allegations or government filing data.
- Large-scale monitoring, scoring/profiling employees, new cross-border transfers, automated decisions, or combining datasets.
- More than one customer in the same data store, personal devices/channels, OCR, browser automation, or a general mailbox.

These categories do not automatically make processing unlawful; they exceed the default pilot boundary and economics.

## Access control and identity

- [ ] Use customer corporate accounts, MFA and named users; no shared passwords.
- [ ] A dedicated shared/collaborative mailbox or portal route is used; no personal inbox or personal WhatsApp.
- [ ] Access is restricted to the cohort and workflow. For Microsoft app-only mail, use Exchange App RBAC to one mailbox. For Google, prefer user OAuth to a dedicated mailbox and avoid domain-wide delegation.
- [ ] Roles are limited to `OPERATOR`, `REVIEWER`, `ADMIN`; only reviewers approve reminder/handoff.
- [ ] Joiner/mover/leaver and emergency revocation procedures are tested.
- [ ] Sergio’s production access is just-in-time/time-bounded, approved, logged and normally disabled.
- [ ] Quarterly is too slow for a one-close pilot: review the access list before start, at cutoff and at offboarding.

## Credentials and integrations

- [ ] OAuth Authorization Code/managed identity is preferred; never request user passwords.
- [ ] Exact scopes and admin grants are captured in the access register.
- [ ] `Mail.ReadWrite`, `Mail.Send`, Gmail modify/send, domain-wide delegation and ERP writes are absent from Blueprint A.
- [ ] Tokens, client secrets and API keys are encrypted in a managed secret store, never source code, `.env` committed files, logs, Sheets or browser storage.
- [ ] Refresh-token rotation/revocation, credential expiry alert and offboarding revocation are rehearsed.
- [ ] Provider terms, plan entitlement, API limits and vendor approval are confirmed before access.

## Application and infrastructure

- [ ] Prefer customer-owned M365/Google configuration; if no runtime is needed, do not deploy one.
- [ ] If A1 is required, use a separate single-customer service and separate paid Postgres in an EU region; do not reuse the Prospecting Engine database.
- [ ] TLS for all external connections; managed encryption at rest; secure cookies/session controls if a UI exists.
- [ ] Network exposure is minimal; webhook endpoints authenticate/signature-check requests, rate-limit and return no sensitive detail.
- [ ] Dependencies/images are pinned and scanned; OS/runtime patch owner and SLA are named.
- [ ] Inbound content is untrusted. Never execute macros/scripts, follow embedded links automatically, or render active content.
- [ ] Attachment allowlist/size cap/malware scan/isolation is mandatory if files ever enter the bridge.
- [ ] Logs exclude bodies, attachments, tokens and sensitive fields. Error tracking is scrubbed before transmission.
- [ ] Dev/test/prod are separated. Production data is never used in development; synthetic test cases cover edge cases.

## Audit and observability

- [ ] Append-only events record actor, action, timestamp, prior/new state, reason and source reference.
- [ ] Automated and human actors are distinguishable.
- [ ] Access/admin/export/deletion/credential events are logged.
- [ ] Dashboard/alerts show stale ingestion, failures, unowned/overdue/blocked cases, reminder suppression and backup status.
- [ ] Audit cannot be edited by normal operators and does not contain source content.
- [ ] Customer can export its queue and audit without Sergio.

## Retention, deletion and mailbox implications

- [ ] Each data category has a purpose, system of record, retention duration and deletion owner.
- [ ] Default operational metadata retention is one close plus the shortest agreed audit/support window; exact duration is contractual, not assumed.
- [ ] Temporary message/attachment content is deleted immediately after approved extraction/review or never copied.
- [ ] Source links/provider IDs can become personal data; delete them with the case unless audit/law requires retention.
- [ ] Mailbox retention (Microsoft Purview/Google Vault) is confirmed with the customer. Extracted Postgres/Excel/Sheet copies do **not** inherit mailbox policies automatically.
- [ ] Legal hold/investigation overrides are customer-instructed and documented.
- [ ] Offboarding exports data to the customer, revokes access, deletes live data/backups according to plan, and supplies deletion evidence.

## Backups and recovery

- [ ] Backup scope excludes unnecessary documents and secrets where possible.
- [ ] Paid managed backups/PITR are enabled if Postgres is used; free-tier absence of backups is not accepted for paying-client production.
- [ ] Restore is tested to a separate instance before the close, with access controls re-applied.
- [ ] Recovery-point/recovery-time expectations and manual fallback are agreed.
- [ ] Backup retention/deletion follows the DPA and offboarding plan.

## Incident handling

- [ ] Customer incident owner, Sergio contact and subprocessor contacts are recorded.
- [ ] Severity, containment, token revocation, evidence preservation, communication and recovery playbook is rehearsed.
- [ ] DPA specifies how quickly Sergio notifies the controller—without undue delay and early enough for the controller’s GDPR assessment/deadline.
- [ ] The controller decides regulator/data-subject notification; Sergio does not make that legal decision.
- [ ] Every suspected breach and notification decision is logged, even if no regulator notification occurs.
- [ ] An incident can disable intake, reminder generation and all external communication independently.

## Subprocessors, location and transfers

- [ ] Final subprocessor list names hosting, database, email platform, monitoring/error tracking, backup and any LLM.
- [ ] Region and actual processing/support locations—not only storage region—are documented.
- [ ] Transfer mechanism and supplementary assessment/controls are documented where data leaves the EEA.
- [ ] Customer receives required notice/approval for subprocessor changes.
- [ ] DPA terms and security documentation for every subprocessor are retained.
- [ ] An LLM provider is absent by default. If later approved, add its purpose, fields, retention/training settings, region, transfer and DPA before use.

## Communications safety

- [ ] Templates are approved and versioned by the firm.
- [ ] Reminder candidate generation is separate from send; a human approves each v1 send.
- [ ] Complete, ambiguous, stopped, blocked and cutoff-reached cases suppress reminders.
- [ ] Cadence and maximum count are bounded; manual override/stop is immediate.
- [ ] No autonomous free-form LLM reply.
- [ ] No personal WhatsApp. WhatsApp Business remains out unless official API, corporate number, DPA/subprocessors, retention and explicit buyer requirement are separately approved.

## Offboarding acceptance

- [ ] Customer-owned export is tested and understandable.
- [ ] OAuth grants, app registration, API keys, vendor invitations and Sergio accounts are revoked.
- [ ] Rules/flows/triggers have a named customer owner or are disabled.
- [ ] Live/backup/log deletion is executed per contract and evidenced.
- [ ] Remaining manual process and unresolved exceptions are handed to the workflow owner.
- [ ] Post-pilot review records value, incidents, support burden and whether to stop, configure more, or authorize a separately scoped next phase.
