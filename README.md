# AI Prospecting Engine

Internal AI-powered B2B prospecting and commercial-learning engine for discovering, researching, qualifying, and reviewing evidence-backed company opportunities without automated outreach.

The current system supports:

- manual company/domain creation
- asynchronous website research
- source and evidence persistence
- deterministic public-signal extraction
- structured AI analysis behind an LLM provider abstraction
- deterministic opportunity and first-customer-fit scoring
- campaign and funnel tracking
- a manual commercial inbox
- historical, buyer-reported discovery sessions
- transparent discovery quantification, readiness blockers, and qualification outcomes
- a commercial scoreboard centred on the first paid pilot and €900 MRR

No automatic outreach sending, contact enrichment, ML, billing, multi-tenancy, Kafka, or Kubernetes is included. Public research evidence and buyer-reported discovery evidence remain separate.

## Architecture

This repository is a small monorepo:

```text
apps/
  api/   FastAPI backend, PostgreSQL models, migrations, research pipeline
  web/   Next.js operator UI
```

The backend is a modular monolith. Domain models live in `apps/api/app/domain`, application workflows in `apps/api/app/application`, and replaceable infrastructure/providers in `apps/api/app/infrastructure` and `apps/api/app/modules`.

For the first milestone, research jobs run in-process via FastAPI background tasks. The job API is already shaped so it can be moved to Celery + Redis without changing the UI contract.

## Local Setup

1. Copy environment files:

```bash
cp .env.example .env
cp apps/web/.env.example apps/web/.env.local
```

1. Start PostgreSQL:

```bash
docker compose up -d postgres
```

1. Install backend dependencies:

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

1. Install frontend dependencies and run the UI:

```bash
cd apps/web
npm install
npm run dev
```

Open `http://localhost:3000`.

## Environment

`DATABASE_URL` must point to PostgreSQL outside tests.

`LLM_PROVIDER` defaults to `stub`, which returns deterministic structured analysis for local development. To use OpenAI, set:

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4.1-mini
```

Secrets must stay in environment variables or secret storage.

## Commands

From the repository root:

```bash
npm run lint
npm run typecheck
npm test
```

Backend-only:

```bash
cd apps/api
ruff check .
pytest
```

Frontend-only:

```bash
cd apps/web
npm run lint
npm run typecheck
npm run build
```

## Commercial Discovery Lab

Open `/commercial` to review the manual outreach state and record real discovery calls. The system never sends messages. Every call creates a new historical session and can conclude that there is no problem, the existing stack already solves it, measurement is required, one of the two workflow hypotheses is worth continuing, or a safely bounded pilot is possible.

The two active hypotheses are:

1. Monthly payroll-close exception control, using the firm's existing A3/Sage/Cegid/Aplifisa/Bilky stack first.
2. Out-of-scope work → approval → execution → invoicing.

Start with:

- [`discovery_first_call_cheatsheet.md`](discovery_first_call_cheatsheet.md)
- [`discovery_playbook_v1.md`](discovery_playbook_v1.md)
- [`discovery_decision_tree.md`](discovery_decision_tree.md)
- [`pilot_candidate_handoff.md`](pilot_candidate_handoff.md)
- [`discovery_engine_implementation.md`](discovery_engine_implementation.md)

The complete commercial operating material is stored as Markdown files at the repository root. Research reports and their JSON evidence snapshots are versioned alongside them so conclusions remain auditable.

## Current Tradeoffs

- In-process jobs are sufficient for the first vertical slice but should move to Celery + Redis before larger batches.
- Website extraction intentionally fetches only a small set of likely-relevant pages and stores excerpts, not full third-party sites.
- The default LLM provider is deterministic so development and tests do not require credentials.
- Authentication is optional for the internal deployment and required when real OpenAI calls are enabled.
- Discovery assessments are transparent rules, not ML scores. Fatal blockers override the numerical readiness total.
- Commercial sessions are entered manually; no buyer pain, baseline, or willingness-to-pay is inferred from public company research.

## Recommended Next Milestone

Run the first real discovery conversation and record it in `/commercial`. Use an existing-stack-solved or no-problem result as valid learning. Do not start technical pilot work until the hard gate in `pilot_candidate_handoff.md` is complete.
