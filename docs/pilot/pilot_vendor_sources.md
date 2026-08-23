# Pilot vendor and platform source register

Research cut-off: **2026-08-23**. This register supports the pre-implementation delivery lab; it is not a representation that any customer has a particular module, plan, version, API entitlement, or configuration.

## Evidence labels

- **CONFIRMED**: the linked vendor/platform owner explicitly documents the capability.
- **PARTIAL**: the source confirms a related capability but not the whole proposed use.
- **NOT FOUND**: targeted searches of public official material found no supporting contract. This does not prove the capability does not exist.
- **UNKNOWN**: customer- or contract-specific fact that discovery must establish.
- **INFERENCE**: an architectural or commercial conclusion derived from confirmed facts; it is not a vendor promise.

“Integrates”, “connected”, or a marketplace listing is never treated as proof of a public API, webhook, supported object, permission, or SLA.

## Wolters Kluwer / A3

| ID | Official source | Confirmed fact and boundary |
|---|---|---|
| WK-01 | [a3asesor Nom product page](https://www.wolterskluwer.com/es-es/solutions/a3asesor-nom) | **CONFIRMED:** a3asesor Nom includes process controls, alerts/task review, reports, and integration with a3HRgo. It does not document a public API on this page. |
| WK-02 | [a3innuva Portal del Empleado](https://www.wolterskluwer.com/es-es/solutions/a3innuva-portal-del-empleado-empresas) | **CONFIRMED:** document viewing/download, vacation/permission requests, personal-data updates, employee onboarding, and entry of variable concepts/absences/IT are plan-dependent portal capabilities. |
| WK-03 | [a3innuva for advisory firms](https://www.wolterskluwer.com/es-es/solutions/a3innuva/asesorias) | **CONFIRMED:** cloud payroll, optional employee portal, electronic signature, dashboard, time control, and direct administration presentation are modular capabilities. |
| WK-04 | [a3innuva Nómina API — getting started](https://a3developers.wolterskluwer.es/doc/a3innuva-n%C3%B3mina/como-empezar/) | **CONFIRMED:** official REST/JSON payroll API exists; it requires a3innuva Nómina **Conectia**, access through WKA, and an OAuth client. |
| WK-05 | [a3innuva Nómina API — OAuth](https://a3developers.wolterskluwer.es/doc/a3innuva-n%C3%B3mina/OAuth/) | **CONFIRMED:** Authorization Code, access and refresh tokens, per-client OAuth provisioning by WK, TLS 1.2+, 60-minute access token and default 30-day refresh token are documented. |
| WK-06 | [Wolters Kluwer Account and API permissions](https://a3developers.wolterskluwer.es/doc/a3innuva-n%C3%B3mina/wolters-kluwer-account/) | **CONFIRMED:** API is for named cloud products, not on-premise applications; Conectia is mandatory; restricted task permissions and company/site/employee limits are possible. |
| WK-07 | [a3innuva Nómina API endpoints](https://a3developers.wolterskluwer.es/doc/a3innuva-n%C3%B3mina/endpoints/) | **CONFIRMED:** GET endpoints include accessible companies, employees, contracts, absences and pays; many POST/PUT/DELETE operations also exist. No close-exception or generic-task endpoint is documented in the published catalogue. |
| WK-08 | [a3innuva Nómina API changelog](https://a3developers.wolterskluwer.es/doc/a3innuva-n%C3%B3mina/changelog/) | **CONFIRMED:** the published changelog says permissions are not distinguished between read and write. This is a material write-risk even if Sergio’s code only issues GET. |
| WK-09 | [a3innuva Nómina API pagination](https://a3developers.wolterskluwer.es/doc/a3innuva-n%C3%B3mina/paginacion/) | **CONFIRMED:** many lists are paginated with a maximum of 50 items per page. A public payroll-specific rate-limit page was **NOT FOUND**. |
| WK-10 | [a3innuva suite and Conectia](https://www.wolterskluwer.com/es-es/solutions/a3innuva) | **CONFIRMED:** the suite advertises Conectia APIs and certified marketplace integrations. This does not prove that every a3 product or module is API-enabled. |

**Research conclusion:** **PARTIAL.** Cloud a3innuva Nómina can support a tightly scoped read-only reconciliation, subject to Conectia, vendor-issued OAuth, and restricted WKA access. Legacy/on-prem a3asesor Nom must use native configuration, reports/exports, or no integration. Payroll webhooks were **NOT FOUND** in the public payroll API documentation; accounting webhooks do not establish payroll webhook availability.

## Sage Despachos Connected

| ID | Official source | Confirmed fact and boundary |
|---|---|---|
| SG-01 | [Sage software for advisory firms](https://www.sage.com/es-es/software-asesorias-y-despachos/) | **CONFIRMED:** Sage Despachos Connected includes internal management, case/task/workload tracking, real-time request follow-up, labor/payroll, document management, and client/employee portals. Availability depends on configuration/modules. |
| SG-02 | [Sage Despachos Connected solution detail (PDF)](https://www.sage.com/es-es/-/media/files/sagedotcom/spain/documents/pdf/generacion_despachos_profesionales.pdf) | **CONFIRMED:** internal management includes cases and tasks; portal/third-party ecosystem is presented as modular. |
| SG-03 | [Sage 200 Portal del Empleado (PDF)](https://www.sage.com/es-es/-/media/images/sagedotcom/spain/es-es/pdf/productos/sage%20200c%20laboral/new/sage200-laboral-modulo-portal-del-empleado.pdf) | **CONFIRMED:** employee data, payroll PDFs, absence/vacation requests, hierarchical validations, roles, submission status, and Excel export are documented for the related Sage 200 portal. Exact applicability to the prospect’s Despachos version is **UNKNOWN**. |
| SG-04 | [Export maintenance screens to Excel](https://es-kb.sage.com/portal/app/portlets/results/viewsolution.jsp?solutionid=230808104954407) | **CONFIRMED:** Sage 200 and Sage Despachos Connected can export many maintenance screens through advanced Excel export. |
| SG-05 | [Active/inactive labor companies Excel report](https://es-kb.sage.com/portal/app/portlets/results/viewsolution.jsp?solutionid=240422073117033) | **CONFIRMED:** Despachos labor company maintenance can be exported to Excel. |
| SG-06 | [Labor alerts and comments](https://es-kb.sage.com/portal/app/portlets/results/botviewsolution.jsp?hypermediatext=null&solutionid=230821074925863) | **CONFIRMED:** Despachos Connected has configurable labor alerts/comments attached to employee records. |
| SG-07 | [External document to employee portal](https://es-kb.sage.com/portal/app/portlets/results/view2.jsp?k2dockey=241017113227670) | **CONFIRMED:** external documents can be placed in document management and published with company/employee access rules. |
| SG-08 | [Sage Tech Partner marketplace](https://marketplacepartners.sage.com/) | **CONFIRMED:** Sage operates a Tech Partner ecosystem including Sage 200 and Despachos Connected. It does not establish a public payroll API. |
| SG-09 | [Sage 200 Spain API authorization](https://developer.sage.com/200c/docs/v1.0.0/guides/authorization) | **CONFIRMED:** an official Sage 200 API and Sage ID authorization exist for Sage 200 installations. Public documentation reviewed did not establish labor/payroll objects or equivalence with Despachos Connected. |

**Research conclusion:** **PARTIAL.** Native tasks, requests, portal, alerts, documents, and Excel exports make `CONFIGURE_EXISTING_STACK` a strong first test. A public Despachos Connected **payroll** API, OAuth contract, payroll webhooks, and safe task/note write endpoint were **NOT FOUND**. Use Sage or its partner before custom integration.

## Bilky

| ID | Official source | Confirmed fact and boundary |
|---|---|---|
| BL-01 | [Bilky for advisory firms](https://bilky.es/asesorias/) | **CONFIRMED:** advisor/company/employee portals, controlled access, document traceability, internal messaging, plans and role configuration are public. |
| BL-02 | [Bilky functionality catalogue](https://bilky.es/funcionalidades/) | **CONFIRMED:** documentation, role permissions, import/export, custom fields/forms, deadline alerts, tickets, attachments, history, and email notifications are listed. |
| BL-03 | [Bilky HR](https://bilky.es/recursos-humanos/) | **CONFIRMED:** employee documents, vacations/absences, communications, incidents/notices and connected portals are documented. |
| BL-04 | [Bilky integrations](https://bilky.es/integraciones/) | **CONFIRMED:** Bilky lists connectors to A3, Sage, Cegid and Aplifisa accounting products. The page does not document API protocol, supported payroll objects, authentication, webhooks, or read/write semantics. |
| BL-05 | [Bilky advisor portal help](https://bilky.es/centro-de-ayuda/portal-asesor-presentacion/) | **CONFIRMED:** authorized users can centralize customers, documents, processes and pending tasks in the browser portal. |

**Research conclusion:** **CONFIRMED for native configuration; NOT FOUND for public API.** Bilky is the closest native fit to a narrow exception queue. A buyer already licensed for the required modules may need configuration and adoption rather than custom software. Vendor-supported connector details must be requested if a residual gap remains.

## Cegid / Diez

| ID | Official source | Confirmed fact and boundary |
|---|---|---|
| CG-01 | [Cegid portal for advisory firms](https://www.cegid.com/ib/es/productos/software-programa-erp-asesorias-gestorias/portal-empleado/) | **CONFIRMED:** payroll/certificate/shared-document viewing, employer–employee messaging, vacations, time control and notifications are documented. |
| CG-02 | [Cegid DiezNOM](https://www.cegid.com/ib/es/productos/software-gestion-nominas-asesorias/) | **CONFIRMED:** payroll/adviser product with updated agreements, portal, payroll/certificate access, vacation requests and individual/mass communications. |
| CG-03 | [Cegid Visualtime document workflow](https://www.cegid.com/ib/es/productos/software-gestion-tiempo-visualtime/) | **PARTIAL:** another Cegid product documents requesting missing documents, photo upload, manager validation, reminders and centralization. It must not be assumed to be included in DiezNOM. |
| CG-04 | [Cegid portal support](https://www.cegid.com/ib/es/asistencia-al-cliente/portal-empleado/) | **CONFIRMED:** official Diez support/commercial channels exist for validating product-specific capability. |

**Research conclusion:** **PARTIAL.** Portal and notifications are real; public DiezNOM API endpoints, OAuth, webhooks, export formats and bounded write operations were **NOT FOUND**. Ask Cegid/Diez support before designing any bridge.

## TeamSystem / Aplifisa

| ID | Official source | Confirmed fact and boundary |
|---|---|---|
| AP-01 | [Aplifisa professional labor software](https://www.aplifisa.com/asesorias/programa-laboral-aplifisa/) | **CONFIRMED:** labor management, email notice module, Doc3W integration and Excel reports are documented. |
| AP-02 | [Aplifisa employee portal](https://www.aplifisa.com/asesorias/aplicacion-portal-empleado/) | **CONFIRMED:** three profiles, employee requests with status, incidents, vacations/leave, data updates, documents, bidirectional communication and traceability. |
| AP-03 | [Mis Documentos 3W](https://www.aplifisa.com/asesorias/aplicacion-gestion-documental/) | **CONFIRMED:** encrypted cloud document sharing, per-client virtual disks, notifications, internal messaging and bidirectional upload/download. |
| AP-04 | [Aplifisa Asesor Laboral](https://www.aplifisa.com/aplifisa-asesor-laboral/) | **CONFIRMED:** mass incidents, Excel export of economic reports, portal/Doc3W links and time-entry import. |
| AP-05 | [Aplifisa support contacts](https://www.aplifisa.com/contacto/) | **CONFIRMED:** a dedicated labor/employee-portal support channel exists and should validate plan/version capabilities. |

**Research conclusion:** **PARTIAL.** Native portal, incident, document, notice and Excel paths are credible. A public payroll API, OAuth, webhook or safe task/note write contract was **NOT FOUND**.

## Microsoft 365 / Outlook

| ID | Official source | Confirmed fact and boundary |
|---|---|---|
| MS-01 | [Microsoft Graph permissions reference](https://learn.microsoft.com/en-us/graph/permissions-reference) | **CONFIRMED:** `Mail.ReadBasic` excludes bodies/attachments; `Mail.Read` is required to read them; delegated shared-mail permissions and application permissions differ. |
| MS-02 | [Delegated/shared folders](https://learn.microsoft.com/en-us/graph/outlook-share-messages-folders) | **CONFIRMED:** delegated `Mail.Read.Shared` can read shared/delegated folders, but shared delegated scopes do not support change-notification subscriptions; application `Mail.Read` is required for subscriptions to shared/delegated mailbox folders. |
| MS-03 | [Graph access modes](https://learn.microsoft.com/en-us/graph/auth/auth-concepts) | **CONFIRMED:** delegated access acts for a signed-in user; app-only access acts as the application and is intended for unattended services. |
| MS-04 | [Exchange App RBAC](https://learn.microsoft.com/en-us/exchange/permissions-exo/application-rbac) | **CONFIRMED:** app-only Exchange permissions can be constrained to a mailbox resource scope; this supersedes legacy Application Access Policies. |
| MS-05 | [Outlook change notifications](https://learn.microsoft.com/en-us/graph/change-notifications-overview) | **CONFIRMED:** message subscriptions can target an inbox/folder; delivery is a notification, not a durable work queue; Microsoft documents a maximum of 1,000 active subscriptions per mailbox across applications. |
| MS-06 | [Subscription creation limitations](https://learn.microsoft.com/en-us/graph/api/subscription-post-subscriptions?view=graph-rest-1.0) | **CONFIRMED:** delegated subscriptions cover the signed-in mailbox; shared/delegated folders require application permission. |
| MS-07 | [Message delta queries](https://learn.microsoft.com/en-us/graph/delta-query-messages) | **CONFIRMED:** incremental sync is per folder and supplies next/delta links. |
| MS-08 | [Lifecycle notifications](https://learn.microsoft.com/en-us/graph/change-notifications-lifecycle-events) | **CONFIRMED:** subscriptions can require reauthorization, be removed, or miss notifications; recovery requires delta/full resync logic. |
| MS-09 | [Get attachments](https://learn.microsoft.com/en-us/graph/api/attachment-get?view=graph-rest-1.0) | **CONFIRMED:** message attachment retrieval requires `Mail.Read`; file/item/reference attachments differ. |
| MS-10 | [Office 365 Outlook Power Automate connector](https://learn.microsoft.com/en-us/connectors/office365connector/) | **CONFIRMED:** shared-mailbox triggers exist, but documented limitations include skipped/duplicated messages, attachment timeouts and protected-mail limitations. |
| MS-11 | [Microsoft Forms and Excel](https://support.microsoft.com/en-us/forms/microsoft-forms-and-excel-workbooks) | **CONFIRMED:** form responses can be stored/synchronized to an Excel workbook in OneDrive or SharePoint. |
| MS-12 | [Exchange retention](https://learn.microsoft.com/en-us/purview/retention-policies-exchange) | **CONFIRMED:** shared/user mailbox messages and attachments can be governed by Purview retention; a copy extracted into a separate pilot store has its own lifecycle. |

## Google Workspace / Gmail

| ID | Official source | Confirmed fact and boundary |
|---|---|---|
| GG-01 | [Choose Gmail API scopes](https://developers.google.com/workspace/gmail/api/auth/scopes) | **CONFIRMED:** `gmail.metadata` excludes bodies; `gmail.readonly` reads messages/settings and is a restricted scope. Server storage/transmission of restricted-scope data can require Google verification/security assessment. |
| GG-02 | [Gmail API reference](https://developers.google.com/workspace/gmail/api/reference/rest) | **CONFIRMED:** APIs exist for messages, threads, labels, history, watch and attachments. |
| GG-03 | [Gmail push notifications](https://developers.google.com/workspace/gmail/api/guides/push) | **CONFIRMED:** push uses Cloud Pub/Sub; watches may be label-filtered, must be renewed at least every seven days, and can delay/drop notifications, requiring periodic history sync. The documented maximum is one notification event per watched user per second. |
| GG-04 | [Gmail history](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.history/list) | **CONFIRMED:** changes can be read after a history ID; stale IDs return 404 and require a full sync. |
| GG-05 | [Gmail attachments](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages.attachments/get) | **CONFIRMED:** attachments require a broad read/modify scope; metadata scope is insufficient. |
| GG-06 | [Service-account security](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts) | **CONFIRMED:** Google recommends avoiding domain-wide delegation where OAuth consent can satisfy the task; domain-wide delegation can impersonate any domain user and is high impact. |
| GG-07 | [Google Groups Collaborative Inbox](https://support.google.com/a/users/answer/10375787?hl=en) | **CONFIRMED:** conversations can be assigned and marked complete/duplicate/no-action using Groups permissions. |
| GG-08 | [Gmail delegated/shared inbox](https://support.google.com/a/answer/11946994?hl=en-GI) | **CONFIRMED:** delegates can read/send/delete a mailbox; delegation is mailbox-wide, not folder-scoped. |
| GG-09 | [Gmail labels and filters](https://support.google.com/mail/answer/9259770?hl=en) | **CONFIRMED:** labels and filters can route and mark messages without an API. |
| GG-10 | [Google Forms to Sheets](https://support.google.com/docs/answer/2917686?hl=en) | **CONFIRMED:** form responses can populate a linked Sheet; form and Sheet permissions must be managed separately. |
| GG-11 | [Google Vault Gmail retention](https://support.google.com/vault/answer/2535539?hl=en) | **CONFIRMED:** Vault can apply Gmail retention rules when licensed/configured. Extracted pilot records are not automatically governed by mailbox retention. |

## Data protection and hosting

| ID | Official source | Confirmed fact and boundary |
|---|---|---|
| DP-01 | [GDPR official text](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | **CONFIRMED:** purpose limitation/data minimization/storage limitation (Art. 5), privacy by design/default (Art. 25), processor terms (Art. 28), security (Art. 32), breach duties (Arts. 33–34), DPIA (Art. 35), and special-category rules (Art. 9). |
| DP-02 | [EDPB controller/processor guidelines](https://www.edpb.europa.eu/documents/guideline/guidelines-072020-on-the-concepts-controller-and-processor-in-the-gdpr_en) | **CONFIRMED:** roles depend on who determines purposes and means, not merely contract labels. |
| DP-03 | [AEPD treatment security](https://www.aepd.es/derechos-y-deberes/cumple-tus-deberes/medidas-de-cumplimiento/seguridad-de-los-tratamientos) | **CONFIRMED:** Art. 32 safeguards must be risk-appropriate across the treatment lifecycle. |
| DP-04 | [AEPD risk/DPIA guide](https://www.aepd.es/guias/gestion-riesgo-y-evaluacion-impacto-en-tratamientos-datos-personales.pdf) | **CONFIRMED:** risk analysis and proportionate controls are treatment-specific; high residual risk may require a DPIA/consultation. |
| DP-05 | [AEPD breach response](https://www.aepd.es/prensa-y-comunicacion/blog/brechas-de-seguridad-de-datos-personales-que-son-y-como-actuar) | **CONFIRMED:** processor/controller breach responsibilities should be in the processing contract and decisions must be recorded. |
| RD-01 | [Render regions](https://render.com/docs/regions) | **CONFIRMED:** Frankfurt is available; existing services/databases cannot simply change region. |
| RD-02 | [Render Postgres encryption](https://render.com/docs/postgresql-creating-connecting) | **CONFIRMED:** AES-256 at rest and TLS for external connections are documented. |
| RD-03 | [Render Postgres backups](https://render.com/docs/postgresql-backups) | **CONFIRMED:** PITR applies to paid databases; free databases lack platform logical backups. |
| RD-04 | [Render deploys](https://render.com/docs/deploys) | **CONFIRMED:** managed deployments and zero-downtime behavior exist; application/database rollback remain separate concerns. |
| RD-05 | [Render cron jobs](https://render.com/docs/cronjobs) | **CONFIRMED:** scheduled jobs use UTC and at-most-one active run per cron service, with a minimum monthly charge. |

## Explicit negative findings

As of the cut-off, public official documentation supporting the following was **NOT FOUND**:

- Sage Despachos Connected payroll REST/GraphQL API, payroll OAuth scopes, payroll webhooks, or safe generic-task write endpoint.
- Bilky public API reference, OAuth/scopes, webhook contract, rate limits, or payroll record semantics.
- Cegid DiezNOM public API reference, OAuth/scopes, webhook contract, export specification, or safe task/note write endpoint.
- Aplifisa labor public API reference, OAuth/scopes, webhook contract, or safe task/note write endpoint.
- a3innuva Nómina payroll webhooks or a generic internal task/note endpoint.

These negative findings require a vendor/partner question, not reverse engineering, database access, or browser automation.
