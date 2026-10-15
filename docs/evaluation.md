# Evaluation

`python -m app.evaluation.evaluators` (from /backend) reports customer-identification accuracy,
Recall@5 / Precision@5 for retrieval, and end-to-end quality-gate success on the mock data.
The benchmark is intentionally small (6 identity cases, 4 retrieval cases, 2 runs). Grow it by adding
synthetic customers/emails/documents under `/data` and cases in `evaluation/test_cases.py`.
Unit/integration tests: `pytest -v`.
