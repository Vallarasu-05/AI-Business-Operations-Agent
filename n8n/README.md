# n8n workflows (starter set)

Each file is a minimal **Webhook -> service node -> Respond to Webhook** workflow.

1. Open http://localhost:5678, then **Workflows -> Import from file** for each JSON here.
2. Open each service node and attach your credentials (Google OAuth, HubSpot). Credentials are never exported.
3. Review node parameters. n8n node schemas change between versions, so treat these as scaffolds, not guaranteed-to-import-clean.
4. Add **Header Auth** on each Webhook node checking `X-Webhook-Secret` equals `N8N_WEBHOOK_SECRET`.
5. Activate the workflow. The backend calls the production URL `http://localhost:5678/webhook/<path>`
   (paths: meeting-trigger, calendar-lookup, gmail-research, crm-lookup, document-research, sales-sheet,
   briefing-delivery, approval).

The agent only calls `briefing-delivery` (in `DATA_MODE=live_write`, after human approval).
The read workflows are optional: the Python integrations call Google/HubSpot directly by default.
