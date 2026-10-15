.PHONY: infra backend frontend test cli eval
infra:
	docker compose up -d
backend:
	cd backend && uvicorn app.main:app --reload --port 8000
frontend:
	cd frontend && npm run dev
test:
	cd backend && python -m pytest -v
cli:
	cd backend && python ../scripts/run_agent_cli.py "Prepare tomorrow's sales meeting with ABC Corporation"
eval:
	cd backend && python -m app.evaluation.evaluators
