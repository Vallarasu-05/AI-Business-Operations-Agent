import pytest
from app.config import settings


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    """Tests always run in mock mode with no LLM."""
    monkeypatch.setattr(settings, "data_mode", "mock")
    monkeypatch.setattr(settings, "llm_api_key", "")
    monkeypatch.setattr(settings, "vector_backend", "memory")
