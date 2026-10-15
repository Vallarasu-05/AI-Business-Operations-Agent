# Security

* **Untrusted content**: email, documents and web text are sanitized (`security/sanitizer.py`), scanned for
  instruction-like sentences (`security/injection_guard.py`), and flagged sentences are never turned into evidence.
  Prompts wrap external text in `<untrusted_content>` tags. Research nodes have no write tools.
* **Three action levels**: Read (auto) -> Generate (auto) -> Write (requires human approval via `interrupt`).
  Without `DATA_MODE=live_write`, "sending" an email only writes a file to `outputs/outbox/`.
* **Least privilege**: Google scopes are read-only. HubSpot private app: read scopes only until you need writes.
* **Secrets**: `.env` and `token.json` are git-ignored. n8n webhooks are protected by a shared-secret header.
* **API auth**: optional `X-API-Key`. Not production auth: add real user auth/rate limiting before exposing it.
* **Source priority**: CRM > internal docs/email/sheets > memory > web. Conflicts are reported, not silently resolved.
* **Known gaps**: PII handling policy, rate limiting, audit-log table, encrypted token storage are not implemented.
