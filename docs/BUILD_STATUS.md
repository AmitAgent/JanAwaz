# Build Status

## Phase 0 — Foundation: DONE
- [x] 0.1 Repository skeleton + README
- [x] 0.2 FastAPI backend, `/health`
- [x] 0.3 Next.js frontend, simple JanAwaz page
- [x] 0.4 `.env.example`, `.env` gitignored
- [x] 0.5 pytest + ruff (backend), eslint + tsc + build (frontend)

Checks run (in the build sandbox):
- backend: `pytest -q` 1 passed; `ruff check .` and `ruff format --check .` clean
- frontend: `npm run lint`, `npm run typecheck`, `npm run build` pass (Next 15.5.29)

Not yet run on your machine; run the README commands once to confirm.

## Next task
1.1 Database connection (Phase 1).
