# AI Prospecting Engine

Internal AI-powered B2B prospecting engine for discovering, researching, qualifying, and reviewing evidence-backed company opportunities.

The first milestone supports:

- manual company/domain creation
- asynchronous website research
- source and evidence persistence
- deterministic public-signal extraction
- structured AI analysis behind an LLM provider abstraction
- a minimal review UI

No automatic outreach sending, contact enrichment, ML, billing, multi-tenancy, Kafka, or Kubernetes is included.

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
```

## Current Tradeoffs

- In-process jobs are sufficient for the first vertical slice but should move to Celery + Redis before larger batches.
- Website extraction intentionally fetches only a small set of likely-relevant pages and stores excerpts, not full third-party sites.
- The default LLM provider is deterministic so development and tests do not require credentials.
- Authentication is omitted because the initial user is Sergio and the app is intended for local/internal use at this stage.

## Recommended Next Milestone

After the manual domain research flow is reliable, add deterministic scoring and the opportunity review workflow:

- OpportunityScore with configurable weights
- `/opportunities` review queue
- approve/reject decisions
- editable evidence-backed outreach drafts
