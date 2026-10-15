# Architecture

```
React UI -> FastAPI -> LangGraph agent -> tools -> providers (mock | Google+HubSpot) -> n8n (writes)
                              |-> RAG (keyword or embeddings; memory or Qdrant)
                              |-> Evidence + conflict detection -> briefing -> quality gate -> human approval -> deliver
```

* **Provider pattern**: `integrations/factory.py` picks mock or live implementations from `DATA_MODE`.
* **State**: raw data lives in `AgentState`; `evidence` and `errors` use reducers so parallel nodes can append.
* **Execution**: `services/execution_service.py` runs the graph in a background thread, records each node
  update as a step, and the UI polls `/api/executions/{id}`.
* **LLM is optional**: with no key, intent parsing, extraction, risk detection and QA are deterministic.
  With a key, intent parsing and the executive summary use the LLM (evidence wrapped as untrusted data);
  the quality gate still verifies every figure.
