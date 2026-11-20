# API Contract

- GET /health -> 200 {"status": "ok"}
- POST /connections/validate
  - body: {"discom": "SBPDCL" | "NBPDCL", "ca_number": "<text>"}
  - 200 {"discom": "...", "ca_number_normalized": "..."}
  - 422 for an unknown DISCOM or an invalid CA Number
  - Stateless: stores nothing and does not reveal whether the connection exists.

Endpoints that link a connection or list a user's connections and complaints need
authenticated users. They are added once login/OTP exists, not before.
