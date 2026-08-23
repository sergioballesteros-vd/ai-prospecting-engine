# Initial Professional Services Offer

> **HISTORICAL / SUPERSEDED HYPOTHESIS:** retained to show how the offer evolved. The generic intake/routing proposal was rejected by the commercial red team; the current hypothesis is [`First Offer v2`](../commercial/first_offer_v2.md).

## Target Customer

Spanish accounting, tax, labour and gestoría firms with roughly 5-50 employees that receive recurring client emails, forms and documents and still depend on manual review, classification, follow-up or data copying.

## Problem Hypothesis

**Hypothesis, not confirmed:** advisory teams lose billable or response time because client requests and documents arrive through email/contact forms/phone follow-ups, then someone manually decides what it is, what is missing, who should handle it, and where the information must be logged.

## Evidence Supporting the Hypothesis

- CE Consulting exposes a broad asesoría network, offices, job/contact pages and GTM.
- Ayuda T Pymes shows many service situations, support phone/contact flows, newsletter capture, partner/media signals and GTM.
- Aselec has a contact form, customer-attention hours and advisory positioning.
- TaxDown, Billin and Anfix show adjacent fiscal/accounting workflows, support tooling, HubSpot/Intercom/Zendesk/GTM and segment-specific onboarding or demo flows.

## Current Likely Workflow

Observed: public sites show contact forms, support/client attention channels, many service lines, and fiscal/accounting/document-heavy services.

Assumption to validate: a human receives each request, reads the message/document, identifies the matter, checks missing information, sends a reply or reminder, and logs or forwards it to the correct advisor/system.

## Desired Business Outcome

- Reduce repetitive manual processing of client requests and documents.
- Reduce copying between email, folders, spreadsheets, CRM or practice-management tools.
- Shorten first-response time and reduce missed follow-ups.
- Standardize intake so advisors receive cleaner, pre-classified work.

## Sergio's Implementation

A small workflow automation for one high-volume intake process:

1. Connect one inbox or form destination.
2. Classify incoming requests by service type, urgency and missing data.
3. Extract structured fields from email text and attached PDFs where practical.
4. Create a tracking record in Google Sheets/Airtable/Postgres or the client's CRM.
5. Draft an acknowledgement or missing-information reply for human approval.
6. Send daily/weekly operational summaries.

Simple architecture: Python scheduled job or FastAPI service, Gmail/Google Workspace API, lightweight database, OCR only if documents require it, LLM extraction only for messy unstructured text, and human approval before any external reply.

## Initial Scope

One workflow, one inbox/form source, 3-5 request categories, one output tracker, one approval path, and one weekly report. Delivery target: days to a few weeks.

## Pricing Hypothesis

- Conservative low implementation: **€1,500-€2,500**.
- Recommended first offer: **€3,000-€4,500**.
- Upper initial range: **€5,000-€7,500** if OCR, CRM integration or multiple flows are included.

## Monthly Recurring Service

Ongoing value: hosting, monitoring, small workflow adjustments, prompt/rule tuning, usage review, error handling, support, API maintenance, and a monthly operations report.

Suggested monthly price: **€300-€600/month**. For the first customer, a practical anchor is **€450/month** after implementation.

## Path to €900/month

1. Two clients at €450/month after two implementation projects.
2. Three clients at €300/month with a narrow, low-support workflow.
3. One larger client at €900/month only if there are several workflows or critical integrations.

Recommended path: **two clients at €450/month**. It keeps the offer realistic for Spanish SMB advisory firms while reaching €900/month without needing an enterprise sale.

## Positioning

One-sentence: Sergio helps advisory firms automate the messy operational workflows between client email, documents and internal systems, so teams spend less time triaging and copying.

30-second explanation: I look for one repetitive workflow where client requests or documents arrive in an unstructured way, then build a small integration that classifies the request, extracts the useful fields, routes it to the right place, and gives the team a clear control view. AI can help with messy text or PDFs, but the value is operational: fewer manual steps, faster response, and cleaner handoffs.

Problem-oriented positioning: operational automation for advisory workflows, not AI transformation.
