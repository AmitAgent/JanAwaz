# JanAwaz — Project Context

Product: Independent citizen grievance assistance platform.
MVP: Bihar electricity complaints only (SBPDCL and NBPDCL).
Stack: Next.js + TypeScript, FastAPI + Pydantic, PostgreSQL.
Architecture: Modular monolith; background workers for long tasks.
Primary keys: Internal UUIDs.
Connection identifier: Unique DISCOM + normalized CA Number.
Evidence: Fresh video required per complaint; assisted alternative goes to human review.
AI: Provider adapters; AI outputs are suggestions, not authorization.
Submission: Never without explicit citizen approval.
Security: A CA Number alone never grants access to complaint history.
Aadhaar: Not required for MVP.

Current phase: Phase 2 - Connections
Completed: Phase 0 foundation, Phase 1 database (models, migrations, services)
Current task: none
Tests: see docs/BUILD_STATUS.md
Next task: 2.1 (see docs/phases/phase-2-connections.md)
Important decisions: See docs/DECISIONS.md
