# Technical Debt After Market Validation

These are observed issues worth addressing only after the manual motion validates pain and commercial demand.

## Data completeness

- The five historical connection requests lack exact sent timestamps and four lack the exact note text. The seed deliberately keeps those fields unknown.
- Verified roles and public profile URLs are missing for the five named buyers; Karma and Carsán still lack an individual buyer.
- Some commercial records do not yet have evidence-backed FirstCustomerFit rows in the active database. They correctly show “Sin score” rather than a fabricated value.

## FirstCustomerFit limitations

- Deterministic weights and penalties are static; they have not been calibrated against won/lost outcomes.
- Confidence is stored separately and is not part of the total. A company with little or no evidence can therefore retain a baseline fit score; the operator must review confidence and evidence before acting.
- Employee count is often unknown, so size fit remains conservative and cannot distinguish many small firms.
- Buyer accessibility is inferred from public signals and location. It does not prove a reachable decision-maker.
- Regex evidence can produce false positives or miss context. Evidence excerpts remain mandatory for review.

Do not change weights until there are enough reviewed prospects and commercial outcomes to evaluate changes without cherry-picking.

## Research execution

- Background work still runs in-process. A server restart can interrupt an active job; moving to a durable queue is justified only when real usage requires it.
- Crawl retries can create duplicate source rows even though evidence fingerprints are deduplicated.
- The new total and crawl deadlines bound work and preserve committed evidence, but an LLM timeout after crawl is recorded as a failed run and still needs a manual retry.

## Commercial event conventions

- Evidence IDs, message version, note type, outreach reason, action, and learning tags are stored in explicit JSON metadata conventions. The application validates them, but the database does not enforce their shape.
- The inbox is single-operator and has no dedicated actor attribution. That matches the current product, but it would be insufficient for a multi-operator audit trail.
- The idempotent current-state seed is an operator command, not an automatic production startup action. Production must be migrated and seeded deliberately.

## Quality coverage

- Backend behavior has focused unit coverage for manual actions, milestones, notes, seed idempotency, pipeline transitions, scoring, and crawl deadlines.
- The commercial page is covered by lint, TypeScript, and production build checks, but it does not yet have browser-level interaction tests.
