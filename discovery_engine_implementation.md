# Discovery Engine / Sales Lab v1 — Implementation Notes

Updated: 2026-08-23

## Purpose

The Discovery Engine is a manual commercial-learning layer. It tests whether monthly payroll-close exception control or out-of-scope work control deserves a paid pilot. It does not prove either hypothesis, send outreach, or modify Evidence Engine and FirstCustomerFit scoring.

## System boundaries

- Public website research remains in `CompanySource`, `Evidence`, `CompanySignal`, and `CompanyAnalysis`.
- A real conversation creates one immutable `DiscoverySession` with `evidence_type=BUYER_REPORTED`.
- A later call creates another session. Existing records are never overwritten.
- Missing metrics remain absent. They are not serialized or calculated as zero.
- Readiness is a transparent 0–2 assessment with a textual reason for every dimension.
- Fatal blockers prevent pilot qualification regardless of readiness total.

## Data model

`DiscoverySession` records:

- prospect, contact, opportunity, occurrence date, hypothesis, and session status;
- workflow, software, structured workflow details, buyer-reported facts and metrics;
- pain examples, objections, alternatives, raw notes, and unresolved questions;
- existing-stack capability and qualification flags;
- calculated metrics with formula and input provenance;
- readiness dimensions, total, blockers, missing information, outcome, and next action.

Migrations:

- `202608230002_commercial_ops.py`: contacts and commercial notes.
- `202608230003_discovery_sessions.py`: historical discovery sessions.
- `202608230004_discovery_workflow_details.py`: structured workflow detail payload.

## API

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/api/commercial/prospects` | Commercial inbox with complete session history |
| `GET` | `/api/commercial/prospects/{company_id}` | One prospect and history |
| `POST` | `/api/commercial/prospects/{company_id}/discovery-sessions` | Append one discovery event |
| `GET` | `/api/commercial/scoreboard` | Activity, discovery outcomes, pilots, setup revenue, and MRR |
| `PUT` | `/api/commercial/prospects/{company_id}/buyer` | Maintain the primary buyer manually |
| `POST` | `/api/commercial/prospects/{company_id}/actions` | Record an action already performed outside the system |

## Qualification outcomes

- `NO_PROBLEM`
- `EXISTING_STACK_SOLVES_IT`
- `MEASURE_FIRST`
- `LABOR_CLOSE_CANDIDATE`
- `OUT_OF_SCOPE_WORK_CANDIDATE`
- `OTHER_WORKFLOW_SIGNAL`
- `PILOT_CANDIDATE`
- `DISQUALIFIED`

The existing stack is tested before a custom pilot. Out-of-scope work needs a buyer-reported example. A pilot candidate needs a recurring problem, usable baseline, confirmed stack gap, sponsor, workflow owner, and bounded safe scope.

Fatal blockers include existing-stack-solved, no usable baseline, no sponsor, no workflow owner, unsafe requirement, unconfirmed/non-recurring workflow, and an unbounded pilot.

## Transparent calculations

The backend returns calculation objects containing `value`, `unit`, `formula`, and `source_fields`.

```text
derived_total_followup_minutes = manual_reminders * minutes_per_reminder
manual_followup_hours = total_followup_minutes / 60
estimated_monthly_followup_cost = manual_followup_hours * buyer_hourly_cost
potential_absorbed_value = out_of_scope_estimated_value - out_of_scope_invoiced_value
```

Every named input must be supplied. Hourly cost is never invented.

## UI flow

`/commercial` presents:

1. Current commercial scoreboard and North Star.
2. Manual outreach groups and prospect selection.
3. Buyer and public research context.
4. Compact Discovery Lab ordered around problem → evidence → quantification → existing stack → decision → next action.
5. Latest outcome, transparent calculations, blockers, missing information, and full session history.

No control in this UI sends outreach.

## Operational workflow

1. Verify a manual acceptance/reply and record it in `/commercial`.
2. Conduct a 20–30 minute call with `discovery_first_call_cheatsheet.md`; do not start with a demo.
3. Save one discovery session immediately after the call.
4. Accept `NO_PROBLEM`, `EXISTING_STACK_SOLVES_IT`, or `MEASURE_FIRST` without forcing a project.
5. For a candidate, involve the workflow owner and close information gaps.
6. Start no technical work until every item in `pilot_candidate_handoff.md` is complete.

## Quality gates

Run before handoff or push:

```bash
cd apps/api
source .venv/bin/activate
ruff check .
pytest
alembic upgrade head

cd ../web
npm run lint
npm run typecheck
npm run build

cd ../..
git diff --check
```

Browser QA target:

```text
/commercial → open prospect → add discovery session → review calculations/blockers/outcome → confirm history and scoreboard
```

Use an isolated database for QA. Never create fake sessions against the operator's real prospect data.

## Current baseline

At implementation completion the local commercial state contains five connection requests sent, zero acceptances, zero conversations, zero real discovery sessions, zero pilots, €0 setup revenue, and €0/€900 MRR. The next objective is the first paid pilot, but the next action is to obtain and record one real conversation without biasing its outcome.
