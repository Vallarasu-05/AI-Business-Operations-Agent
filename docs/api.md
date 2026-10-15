# API

| Method | Path | Purpose |
|---|---|---|
| GET | /health | status, data mode |
| POST | /api/agent/run `{request}` | start a run, returns `execution_id` |
| GET | /api/executions | list runs |
| GET | /api/executions/{id} | status, steps, state, pending interrupt |
| POST | /api/approval/{id} `{status: approved/edited/rejected, email_body?}` | resume after human review |
| GET | /api/meetings/tomorrow | tomorrow's meetings |
| GET | /api/meetings/{event_id} | one meeting |
| GET | /api/briefings/{id} | structured briefing + quality |
| GET | /api/briefings/{id}/markdown | markdown briefing |
| GET | /api/briefings/{id}/pdf | PDF (after delivery) |

If `API_KEY` is set, send `X-API-Key`. Interactive docs: http://localhost:8000/docs
