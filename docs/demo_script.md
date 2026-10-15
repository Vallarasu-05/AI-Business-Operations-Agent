# Demo script (3 minutes)

1. Show the planted data: CRM deal 18L, an email claiming 20L, an email with a hidden prompt injection.
2. Run: "Prepare tomorrow's sales meeting with ABC Corporation". Narrate the live timeline (parallel research).
3. Open the briefing: point at [E#] citations, the **Data Conflicts** section, the **prompt-injection** risk.
4. Show the quality gate JSON (grounding, hallucination risk).
5. Human approval: edit the email draft, approve. Show `outputs/outbox/` and `outputs/briefings/*.pdf`.
6. Re-run: **Customer Memory** now lists concerns from the previous meeting.
7. Run `python -m app.evaluation.evaluators`.
