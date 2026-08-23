# Project status

**Date:** 2026-08-23

**Phase:** Commercial validation checkpoint; return to market

**North Star:** €900 MRR

**Near-term objective:** First paid pilot

## Current funnel

| Sent | Accepted | Conversations | Discoveries | Pilot candidates | Paid pilots | Setup revenue | MRR |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 0 | 0 | 0 | 0 | 0 | €0 | €0 / €900 |

These values come from the local persisted commercial state. They are not projections.

## Current direction

- **ICP hypothesis:** independent Spanish advisory/accounting/payroll firms with roughly 5–15 employees, recurring payroll work, a named sponsor and workflow owner, and a measurable exception gap not already solved by their licensed stack.
- **Primary hypothesis:** monthly payroll-close exception control.
- **Secondary hypothesis:** out-of-scope work → scope check → approval → execution → invoicing. Discovery only; not a product.
- **Offer hypothesis:** configure one bounded monthly close and its exception control, using the customer's existing stack first.
- **Default architecture:** Blueprint A0 — customer-owned intake → deterministic metadata checklist → narrow exception queue → named owner → human review → manual payroll handoff.
- **Pricing hypothesis:** €1,000 setup + €200/month. This has not been validated by a buyer.

## Validated at this checkpoint

- Five manual LinkedIn connection requests are represented in the commercial state.
- The application can preserve manual funnel actions and buyer-reported discovery sessions separately from public research.
- The discovery system has explicit safe outcomes, quantification, blockers, and pilot-readiness gates.
- Public vendor research supports an existing-stack-first approach and rejects a generic replacement portal as the default.
- A metadata-first, no-write-back pilot blueprint and its security, failure, implementation, and economic boundaries are documented.

## Not validated

- No buyer has accepted, replied, completed discovery, qualified, or paid.
- Pain frequency, baseline, willingness to pay, ROI, offer wording, and price are not buyer-validated.
- No prospect has demonstrated an unresolved gap after its current A3/Sage/Bilky/Aplifisa/Cegid configuration is reviewed.
- Blueprint repeatability, support load, and recurring value remain unproven.

## Active blockers

- Zero buyer-reported evidence.
- Exact send timestamps/note text and several buyer identities remain incomplete.
- No completed [`pilot_candidate_handoff`](docs/pilot/pilot_candidate_handoff.md).
- No approved cohort, owner, baseline, access plan, or commercial authorization for implementation.

## Next manual action

Review the five LinkedIn connection requests already sent and wait for buyer-reported evidence. Record only what actually happens.

The canonical documentation index is [`docs/README.md`](docs/README.md).

## Rule

**NO BUILD until new buyer-reported evidence justifies a product-changing action.**
