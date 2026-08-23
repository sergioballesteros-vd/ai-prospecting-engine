# Commercial Operations Status

Updated: 2026-08-23

## North Star

External monthly recurring income: **€0 / €900 MRR**.

The operating objective is one validated, narrow workflow problem that can become a paid first engagement. Volume of companies, messages, or AI calls is not the target.

## Current hypotheses

The original generic intake/chasing offer has been rejected. The primary hypothesis is monthly payroll-close exception control, using the software already paid for first. The secondary hypothesis is out-of-scope work → approval → execution → invoicing. Neither is buyer-validated yet.

`NO_PROBLEM`, `EXISTING_STACK_SOLVES_IT` and `MEASURE_FIRST` are valid outcomes. Public research only prepares questions; only a historical discovery session can store buyer-reported pain, baselines or willingness.

## Five connection requests sent manually

| Company | Buyer | State | Note record |
| --- | --- | --- | --- |
| CE Consulting | Jesús Ignacio | Connection sent | Sent with note; exact text and send time were not supplied |
| Aselec Consultores | Alberto Torrecillas | Connection sent | Sent with note; exact text and send time were not supplied |
| Gestoría DS | Diego Domínguez | Connection sent | Sent with note; exact text and send time were not supplied |
| Gaudium Asesores | Marta Gómez | Connection sent | Sent with note; exact text and send time were not supplied |
| OK Asesores | David Lahuerta | Connection sent | Sent without a note; exact send time was not supplied |

No acceptance, reply, meeting, proposal, win, or loss has been recorded for these five.

No discovery call, hypothesis candidate or pilot has been recorded. Setup revenue and MRR remain €0.

## Rejected or skipped

| Company | State | Recorded reason |
| --- | --- | --- |
| Ayuda T Pymes | Lost / skipped | Rejected for first-customer fit |
| GD Asesoría | Lost / skipped | Rejected for first-customer fit |

Do not infer a more specific reason until Sergio records one from the actual review.

## Buyer-resolution queue

- Karma Asesores: the role hypothesis is Managing Partner / Socio Director; no LinkedIn profile was found.
- Carsán Gestión: good prospect and standard-software integration hypothesis; the individual buyer remains unresolved.

## Operating system state

- `/commercial` groups prospects into To Contact, Connection Sent, Accepted, Replied, Meeting, Proposal, Won, and Lost / Skipped.
- The UI records manual actions only. It cannot send outreach.
- Each real call creates an immutable buyer-reported discovery session; existing research evidence remains separate.
- Both hypotheses have compact structured branches, transparent calculations, missing-information prompts, readiness reasons, fatal blockers and explicit outcomes.
- The scoreboard tracks connections, conversations, discovery outcomes, candidates, proposed/paid pilots, setup revenue and MRR. The immediate objective is the first paid pilot.
- Buyer name, role, and profile URL can be maintained without collecting unnecessary personal data.
- Connection-note type, exact message when known, message version, selected evidence, outreach reason, milestone timestamps, rejection reason, manual notes, and learning tags are traceable.
- The current records are seeded idempotently with `cd apps/api && python -m app.application.commercial_seed` after migrations.
- The local database has been migrated and seeded. Production is compatible but has not been changed or deployed in this work.

## Known information gaps

- Exact contacted dates for the five connection requests.
- Exact text of the four connection notes.
- Verified roles and profile URLs for the five named buyers.
- Individual buyers for Karma Asesores and Carsán Gestión.
- FirstCustomerFit scores for records that have not been researched in the active database.
- Whether either surviving workflow is recurrent and valuable in a real buyer conversation.
- Which functions the five prospects have configured and actually adopted in A3/Sage/Cegid/Aplifisa/Bilky or their current stack.
- Any usable baseline, sponsor, workflow owner, safe bounded cohort or willingness-to-pay.
