# Pilot technical discovery questions

Ask these only after commercial pain is validated. Answers must be demonstrated or evidenced where possible; “it integrates” is not an API answer.

## MUST KNOW BEFORE ESTIMATE

### Scope and outcome

1. What exact monthly-close workflow is in scope, from request through payroll handoff and closure?
2. What is the last real example? Where did it wait, duplicate, go missing or require rework?
3. What single cohort is included? How many client companies/employees/items per close?
4. What is the payroll period, request date, cutoff, timezone and escalation point?
5. What baseline exists: incomplete/late clients, touches, minutes, cutoff misses and source/owner?
6. What metric/target defines success, and who owns measurement?
7. Who is sponsor, daily owner, reviewer, backup and final approver?
8. What must remain manual? What would make the buyer stop the pilot immediately?

### Payroll and current stack

9. Exact vendor, product name, version/build and deployment: cloud/SaaS, hosted, desktop or on-prem?
10. Is this a3asesor Nom or cloud a3innuva Nómina? Sage Despachos Connected or related Sage 200 module? Exact Diez/Aplifisa/Bilky modules?
11. Which labor, portal, document, task/case, alert, report/export and integration modules are licensed and enabled?
12. Demonstrate the current portal: forms/requests, documents, owners, status, deadlines, reminders, audit and exports.
13. Has vendor/partner support already tried to configure this outcome? What was the documented gap?
14. Who is the vendor/partner contact, and can they confirm plan/version capability in writing?
15. What official export/report is available? Exact columns, format, encoding, delivery, frequency and stable IDs?
16. Is an official API included in the customer plan? Provide official documentation/Swagger, supported objects, environment and contract—not screenshots of “integration” marketing.
17. For API: auth flow, OAuth client approval, scopes/roles, read-only separation, company/cohort restriction, rate limits, webhooks, audit, sandbox and SLA?
18. Can all required outcome be achieved with portal configuration plus Excel/Sheets before custom code?

### Intake, email and collaboration

19. Is the firm on Microsoft 365/Exchange Online, Google Workspace/Gmail, another hosted provider or on-prem mail?
20. Is there a dedicated corporate shared mailbox, mailbox folder, Google Group Collaborative Inbox, portal route or form? Who owns it?
21. Are emails mixed with unrelated/sensitive work? Can a new dedicated address/label/folder be required for the pilot cohort?
22. Which current Excel/Sheets/task file is used? Where is it hosted; who owns, edits, reviews and exports it?
23. Can Microsoft Forms/Google Forms be used? Who may respond, and how are responders authenticated/mapped?
24. What identity platform/MFA/Conditional Access/admin-consent rules apply?
25. Which permissions will security approve? Is app-only mailbox access or Google domain-wide delegation prohibited?
26. What retention/eDiscovery/Vault rules apply to the mailbox, form, Sheet/Excel and copied metadata?
27. Are Power Automate/Apps Script/native automation allowed and licensed? Who owns flows/triggers after offboarding?
28. What channels are approved for reminders? Confirm personal WhatsApp is out.

### Data and security

29. List every proposed field/document. Which can be replaced by controlled status codes or source references?
30. Will salary, bank, tax/national/Social Security ID, health/IT/medical, union, garnishment, contract or dependant data be present?
31. Can source documents remain in the existing portal/mailbox while the queue stores metadata only?
32. Who is controller/processor; is the DPA ready; what employee/client notices and lawful basis are relied on?
33. Required hosting/support regions, subprocessors, transfer restrictions, certifications and security questionnaire?
34. Required encryption, access review, audit, backup, recovery, incident notification, deletion and offboarding controls?
35. Can production access be time-bounded and synthetic data used for all development/testing?
36. Does the risk assessment require a DPIA or security review before access?

### Operations and economics

37. Who manually resolves each exception category, and what happens if that owner is absent?
38. What reminder cadence/templates/maximum/stop rules are approved, and who approves each v1 send?
39. What manual fallback operates when mailbox, portal, export, API or pilot service is unavailable?
40. Is a test tenant/test company/test mailbox available? If not, what controlled rehearsal is acceptable?
41. What implementation hours/client coordination are realistically available inside the setup fee?
42. What exactly is included in €200/month: monitoring, close review, report, support hours, small changes?
43. Who accepts change orders, and what requested changes automatically re-scope the pilot?
44. If the existing tool solves it, will the buyer accept a configuration-led outcome rather than custom software?

## Required evidence pack before quote

- Product/version/module/license screenshots or admin export.
- Vendor/partner contact and official capability/API/export documentation.
- One anonymized current-state example and cohort schema.
- Current form/email/template/Excel/task artifacts with personal data removed.
- Baseline and success-metric worksheet.
- Data inventory, approved fields/channels, retention and access decision.
- Named sponsor/owner/reviewer/backup and cutoff calendar.
- Manual fallback and kill criteria.

If these are incomplete, quote only a paid discovery/configuration assessment or return to `MEASURE_FIRST`; do not quote an API integration.

## CAN DISCOVER DURING IMPLEMENTATION

These details may be refined after the estimate only if they cannot materially change permissions, risk, architecture or scope:

- Exact display labels, column order, colors and saved views.
- Minor controlled exception-code wording within the agreed category count.
- Report layout and daily summary time.
- Which trained backup operator covers each day.
- Template tone edits that do not change channel/cadence/legal meaning.
- Dashboard grouping and non-sensitive filters.
- Synthetic edge cases added to the test pack.
- Small usability improvements within the change budget.
- Final runbook screenshots and training sequence.

## Questions that immediately force re-estimation

- “Can we add another payroll system/client cohort/workflow/channel?”
- “Can it update salary/employee/payroll fields or file to government?”
- “Can it read the whole mailbox/domain or use our shared password?”
- “Can AI decide whether the information is legally/payroll correct?”
- “Can it send reminders/replies without review?”
- “Can you scrape the UI because the API is unavailable?”
- “Can it store all documents just in case?”
- “Can the same instance serve another customer?”
- “Can monthly support include unlimited changes/general IT?”

Each answer is no under the current pilot; it requires refusal or a new commercial/security scope.
