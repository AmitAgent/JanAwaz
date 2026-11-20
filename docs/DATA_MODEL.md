# Data Model

All primary keys are internal UUIDs. All tables except `audit_events` have `created_at` / `updated_at`.

## users
Citizen account (identity only). `preferred_language`, `is_active`.

## contact_methods
Email or mobile of a user. Unique on (`kind`, `value`); `kind` is `email` or `mobile`.

## connections (Phase 2)
An electricity connection. `discom` (`SBPDCL` or `NBPDCL`) + `ca_number_normalized`, unique together.
Only the normalized CA Number is stored. CA Numbers never go into audit events.

## user_connections (Phase 2)
Link between a user and a connection they claimed. Unique on (`user_id`, `connection_id`).
Many users can link the same connection. A link never exposes other users' complaints.

## complaints
Citizen complaint (drafts only so far). `user_id` (required), `connection_id` (optional, Phase 2),
`status`, `category`, `title`, `description`. A complaint may only use a connection its user has linked.

## audit_events
Append-only log: `actor_user_id`, `action`, `entity_type`, `entity_id`, `event_metadata`.
Actions so far: `complaint.draft_created`, `connection.created`, `connection.linked`.
