# JanAwaz

Independent citizen grievance assistance platform. MVP scope: Bihar electricity complaints (SBPDCL, NBPDCL).

Modular monolith: `backend/` (FastAPI) + `frontend/` (Next.js). See `docs/` for context and the phased plan.

## Run locally

Backend:
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
# http://127.0.0.1:8000/health
```

Frontend:
```bash
cd frontend
npm install
npm run dev
# http://localhost:3000
```

## Checks
```bash
cd backend && pytest -q && ruff check . && ruff format --check .
cd frontend && npm run lint && npm run typecheck && npm run build
```
