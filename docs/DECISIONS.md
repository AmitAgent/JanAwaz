# Decisions

- Phase 0: no AI, Redis, object storage, or cloud deployment (per plan).
- Backend tooling: pytest + ruff (lint and format). Config via pydantic-settings.
- Frontend tooling: Next.js App Router, TypeScript, ESLint, `tsc --noEmit`.
- Phase 2: a connection is unique on (DISCOM, normalized CA Number). Only the normalized value is stored.
- Phase 2: users claim connections through a `user_connections` link table (many users per connection).
- Phase 2: a CA Number alone never grants access. Linking a connection shows the user only their own
  complaints on it, never anyone else's. Complaints may only use a connection their user has linked.
- Phase 2: CA Number rule is generic for now (5-20 letters/digits after removing spaces and separators).
  Tighten per DISCOM in `app/services/ca_number.py` once real formats are confirmed.
- Phase 2: no link/list endpoints yet because there is no authentication. Taking a user id from the
  request body would be unsafe. They follow with login/OTP.
