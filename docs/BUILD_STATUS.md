# Build Status

## Phase 0 — Foundation: DONE

- [x] 0.1 Repository skeleton + README
- [x] 0.2 FastAPI backend, `/health`
- [x] 0.3 Next.js frontend, simple JanAwaz page
- [x] 0.4 `.env.example`, `.env` gitignored
- [x] 0.5 pytest + ruff (backend), eslint + tsc + build (frontend)

## Phase 1 — Database foundation: DONE

- [x] 1.1 Database connection (`DATABASE_URL`, settings, SQLAlchemy session)
- [x] 1.2 Models: user, contact method, complaint, audit event
- [x] 1.3 Alembic setup + initial migration `0001_initial_foundation`
- [x] 1.4 Services: complaints, audit logging
- [x] 1.5 Tests: models and migrations
- [x] 1.6 `alembic upgrade head` verified against PostgreSQL 16 (Docker, port 5433)

Checks run on the dev machine (2026-11-20):

- backend: `pytest -q` 9 passed; `ruff check .` and `ruff format --check .` clean
- migration: `0001` applied to a fresh Postgres 16; tables users, contact_methods, complaints, audit_events created
- frontend: not re-run in Phase 1

Merged in PR #1 (`feature/phase-1-database`).

## Next task

Phase 2 (see `docs/phases/`).
