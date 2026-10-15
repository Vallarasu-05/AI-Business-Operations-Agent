"""Optional LLM layer. With no LLM_API_KEY the agent runs on deterministic logic only."""
import logging
from datetime import date
from pydantic import BaseModel
from app.config import settings
from app.security.sanitizer import UNTRUSTED_NOTICE, wrap_untrusted

log = logging.getLogger(__name__)


class Intent(BaseModel):
    task: str = "meeting_preparation"
    date: str
    meeting_type: str = "sales"
    output: str = "briefing"
    customer_hint: str | None = None


def get_llm():
    if not settings.llm_api_key:
        return None
    try:
        if settings.llm_provider == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model=settings.llm_model, api_key=settings.llm_api_key, temperature=0)
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=settings.llm_model, google_api_key=settings.llm_api_key, temperature=0)
    except Exception as e:  # missing package, bad key format ...
        log.warning("LLM unavailable: %s", e)
        return None


def llm_parse_intent(request: str) -> dict | None:
    llm = get_llm()
    if not llm:
        return None
    try:
        out = llm.with_structured_output(Intent).invoke(
            f"Today is {date.today().isoformat()}. Convert this request to structured intent. "
            f"Dates must be ISO (YYYY-MM-DD).\nRequest: {request}")
        return out.model_dump()
    except Exception as e:
        log.warning("intent LLM failed: %s", e)
        return None


def llm_summary(customer: str, evidence: list[dict]) -> str | None:
    """Writes the executive summary from evidence only. Evidence is wrapped as untrusted data."""
    llm = get_llm()
    if not llm:
        return None
    try:
        block = "\n".join(f"[{e['id']}] ({e['source']}) {e['claim']}" for e in evidence[:40])
        prompt = (f"You are a sales intelligence analyst. {UNTRUSTED_NOTICE}\n"
                  f"Write a 3-sentence executive summary for a meeting with {customer}. Use ONLY the evidence; "
                  f"do not invent facts or numbers; if sources disagree say so.\n\n{wrap_untrusted(block, 'evidence')}")
        return llm.invoke(prompt).content.strip() or None
    except Exception as e:
        log.warning("summary LLM failed: %s", e)
        return None
