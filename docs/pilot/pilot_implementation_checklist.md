# Pilot implementation checklist

Use only after all are true: `PILOT_CANDIDATE`, completed [pilot_candidate_handoff.md](./pilot_candidate_handoff.md), and Sergio’s explicit commercial approval. This checklist does not itself authorize production access or deployment.

## Before technical work

### Commercial and operational gate

- [ ] Signed scope names one workflow, payroll product/version/environment, client cohort and monthly close.
- [ ] Sponsor, workflow owner, backup owner, implementation contacts and escalation path are confirmed.
- [ ] Current-state map covers request → receipt → completeness check → exception → reminder → approval → payroll handoff → close.
- [ ] Last real case and baseline are documented: cohort size, missing/late items, touches, minutes, cutoff misses and source/owner.
- [ ] Success metric, target, measurement method, observation window and kill criteria are signed.
- [ ] In-scope/out-of-scope, change-control and support boundaries are explicit; no general IT support or unlimited changes.
- [ ] Existing-stack configuration test is completed or scheduled first with vendor/partner where appropriate.

### Privacy and security gate

- [ ] Controller/processor roles, DPA, lawful instructions, subprocessor list, region/transfers and security owner are approved.
- [ ] Data inventory confirms metadata-only default; prohibited/special categories and escalation are documented.
- [ ] Retention/deletion, backups, incident response, offboarding and production-access procedures are approved.
- [ ] Corporate accounts, MFA, dedicated mailbox/form/portal route, least-privilege grants and revocation owner are ready.
- [ ] Synthetic test data and test route/environment exist; production content will not be used for development.

### Delivery readiness

- [ ] Exact cohort file/IDs, payroll period, cutoff/timezone, required-item checklist and controlled exception codes are frozen for v1.
- [ ] Approved reminder templates, cadence, maximum reminders, quiet/stop rules and approvers are ready.
- [ ] Manual fallback sheet/export and payroll handoff procedure are written.
- [ ] Access can be obtained without shared password, personal inbox, personal WhatsApp, RPA or unrestricted mailbox/domain scope.
- [ ] Estimate fits roughly 3–7 working days and €1,000 boundary, or a written change order exists.
- [ ] Blueprint selected: A0 by default; A1/B require explicit residual-gap evidence. Blueprint C is rejected.

## Day 1 — map, configure, freeze the contract

- [ ] Walk one recent close case with operator and reviewer; mark every system, wait, decision, owner and duplicate entry.
- [ ] Ask vendor/customer admin to demonstrate licensed portal/task/export capabilities. Record `CONFIGURE_EXISTING_STACK`, `GAP`, or `UNKNOWN` for each required behavior.
- [ ] Choose approved intake route and system of record. Create customer-owned group/shared mailbox/form/file, not personal assets.
- [ ] Freeze v1 fields, states, transition permissions, checklist version and idempotency key.
- [ ] Create synthetic cohort and scenarios: complete, partial, duplicate, unknown company, contradictory, unreadable attachment, owner absent, cutoff reached.
- [ ] Confirm no salary/ID/bank/health/document bytes enter the queue.
- [ ] Define baseline snapshot and daily/close report.
- [ ] Hold end-of-day go/no-go: if native stack solves it, finish configuration/training and do not build A1.

## Day 2 — configure intake and narrow queue

- [ ] Configure portal/form fields, Gmail labels/filters or Outlook folders/rules for the dedicated route.
- [ ] Configure customer-owned Excel/Sheet/native task table with validation, protected columns, views and owners.
- [ ] Implement/configure deterministic completeness rules only; no LLM.
- [ ] Add exact source reference, created/updated timestamps and change/audit mechanism.
- [ ] Add duplicate protection and quarantine for unknown/mismatched mapping.
- [ ] Configure roles and test least privilege with an operator and reviewer account.
- [ ] Prove operator can export/recover the queue without Sergio.
- [ ] If A1 is approved, prepare separate single-customer infrastructure/secrets; do not touch the Prospecting Engine database or production.

## Day 3 — reminder review and failure safety

- [ ] Build/configure reminder **candidate** view from states, due date, last contact and count.
- [ ] Enforce suppressions: complete, needs review, blocked, stop flag, max count, cutoff reached and ambiguous response.
- [ ] Load only approved templates; variables are controlled and previewed.
- [ ] Require human approval; v1 has no autonomous send or free-form generation.
- [ ] Configure owner-absence and cutoff escalation.
- [ ] Exercise kill switches independently: stop intake, stop reminders, revoke access.
- [ ] Test duplicates, out-of-order responses, invalid attachments, revoked permission, stale data and recovery to manual fallback.
- [ ] Verify logs/audit contain no secrets or source content.

## Day 4–5 — rehearsal, security verification and rollback

- [ ] Run a full synthetic rehearsal from intake through manual payroll handoff and closure.
- [ ] Reconcile every source item to exactly one queue outcome; investigate missing/duplicate records.
- [ ] Run table-top failures: mailbox/API unavailable, owner absent, contradictory data, cutoff with open exceptions, wrong reminder candidate, outage and credential expiry.
- [ ] Rehearse code/config rollback and data recovery separately.
- [ ] Restore a backup/export into an isolated location and verify access controls.
- [ ] Confirm customer admin can revoke every grant/token/account and knows where.
- [ ] Complete privacy/security checklist and record accepted residual risks.
- [ ] Measure operator time/usability; remove fields/steps that do not serve the one workflow.
- [ ] Freeze pilot configuration, templates and checklist version. No scope expansion.

## Day 6–7 — training and controlled first close

- [ ] Train primary/backup operator and reviewer using a one-page runbook.
- [ ] Train: meaning of `COMPLETE` vs `APPROVED`, ambiguity escalation, reminder suppression, manual fallback, cutoff report and incident contact.
- [ ] Conduct supervised production smoke test with the smallest approved subset; no payroll write.
- [ ] Verify first input, duplicate handling, owner assignment, checklist, audit and reminder suppression.
- [ ] Hold a pre-cutoff review: counts by state, unowned/overdue/blocked cases, stale connectors and fallback readiness.
- [ ] Customer reviewer approves each first-close handoff/reminder action.
- [ ] Record baseline vs observed metrics without claiming causality from one close.
- [ ] Obtain acceptance or stop/re-scope decision; list defects separately from enhancements.

## First-month operation

- [ ] Daily during close: verify last intake/reconciliation time, failures, unowned/overdue/blocked cases and reminder queue.
- [ ] At cutoff: issue open-exception report; fail closed on uncertainty; use manual process where needed.
- [ ] After close: reconcile source, queue and handoff counts; review incorrect/missed reminders and operator workarounds.
- [ ] Weekly only if needed: approved small checklist/template corrections; no new workflow.
- [ ] End of month: report outcome, support hours, incidents, false positives/negatives, adoption and economic fit.
- [ ] Decide `STOP`, `CONFIGURE_MORE`, `CONTINUE_A`, or separately scope B. Do not drift into C.

## Acceptance tests

- [ ] Same source event delivered twice creates one case/effect and a duplicate audit event.
- [ ] Unknown company/period never auto-maps or advances.
- [ ] Missing required code yields `PARTIAL`; presence yields `COMPLETE`, never `APPROVED`.
- [ ] Only reviewer can approve; every transition has actor/reason/time.
- [ ] Complete/blocked/stopped/cutoff cases create no reminder candidate.
- [ ] Revoked mailbox/API access creates a visible alert and stale state, not silent completeness.
- [ ] Unreadable/protected/oversized attachment produces human review without execution/OCR/storage.
- [ ] Outage/manual fallback can operate through the cutoff and later reconcile safely.
- [ ] Rollback does not delete or rewrite audit history.
- [ ] Customer can export, revoke access and offboard without vendor lock-in to Sergio.

## Stop/re-scope triggers during delivery

- [ ] Stop if production data exceeds approved categories or a special-category document enters the bridge unexpectedly.
- [ ] Stop if a required permission is broader than approved or cannot be restricted/revoked.
- [ ] Stop if workflow ambiguity could affect payroll and the owner cannot resolve it before cutoff.
- [ ] Re-scope if a second system/cohort/workflow/channel appears.
- [ ] Re-scope/reprice if effort exceeds the approved cap, vendor access is delayed, or maintenance cannot fit €200/month.
- [ ] Recommend the native/vendor tool if configuration covers the outcome.

## Completion pack

- [ ] One-page operator runbook and escalation contacts.
- [ ] Frozen field/state/checklist/template/cadence definitions.
- [ ] Access and subprocessor register.
- [ ] Test/rehearsal evidence and known limitations.
- [ ] Rollback/manual fallback/incident/offboarding runbooks.
- [ ] Baseline and first-close measurement report.
- [ ] Signed acceptance or stop/re-scope record.
