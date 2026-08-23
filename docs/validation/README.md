# Validation artifacts

This directory preserves intentionally versioned validation outputs. They are evidence of dated runs, not live application state or current outreach instructions.

## Artifact classification

### A — reproducible fixture/input

| Path | Purpose |
|---|---|
| `apps/api/app/data/outreach_templates.json` | Bounded manual outreach templates used by the application and tests. |
| `apps/api/app/data/validation_spanish_training_companies.csv` | Reproducible validation cohort. |
| `apps/api/data/first_customer_madrid_advisory_candidates.csv` | Reproducible Madrid first-customer campaign input. |

### B — valuable validation artifact

The Markdown reports in this directory and JSON files under [`artifacts/`](artifacts/) preserve tournament, evidence-engine, market-validation, professional-services, and first-customer-fit results. They remain committed so earlier decisions can be audited without pretending the rankings are current.

### C — temporary/local runtime artifact

The following are intentionally excluded from version control:

- `apps/api/prospecting.db` — current local operator database; its aggregate funnel is documented, but the database is not portable project truth.
- `apps/api/first_customer_campaign.db` and `apps/api/prospecting_tournament.db` — reproducible local campaign/tournament databases.
- `.codebase-memory` working changes, `graft/`, caches, logs, `.next`, `node_modules`, and other build output.

### D — sensitive/local configuration

`.env`, `.env.local`, credentials, API tokens, database URLs, OAuth secrets, `.vercel` linkage, and production/local dumps must not be committed. Example environment files may contain placeholders only.

## Reproduction boundary

Scripts, fixtures, migrations, and versioned outputs are retained. Local SQLite files are not. Reproducing an external-research run may also require current public websites, provider access, and explicit credentials supplied outside Git; results may therefore differ over time.
