"""Deterministic signal extraction from untrusted text -> Evidence dicts."""
import re
from app.schemas.evidence import Evidence
from app.security.injection_guard import scan
from app.services.money import parse_amounts

RULES = [
    ("competitor", r"another vendor|competitor|alternative vendor|evaluating (?:other|another)"),
    ("decision_deadline", r"decision by"),
    ("objection", r"discount|too expensive|pricing|budget|cost concern"),
    ("requirement", r"\bapi\b|integration|\bsso\b|saml|data residency|\berp\b|\brest\b"),
    ("timeline", r"timeline|go-live|deploy|\d+ weeks|\d+ months"),
    ("pending_decision", r"to confirm|pending|please confirm"),
    ("preference", r"private cloud|we prefer|prefers"),
    ("commitment", r"action item|will share|will send|to share"),
]
EMAIL_TOPICS = {"competitor", "decision_deadline", "objection", "requirement", "timeline",
                "pending_decision", "preference", "commitment"}
DOC_TOPICS = {"requirement", "timeline", "pending_decision", "preference", "commitment"}
PRICE_WORDS = re.compile(r"price|total|deal|cost|value|worth|proposal|implementation", re.I)


def extract_signals(text: str, source: str, source_id: str, date: str | None,
                    confidence: float, allowed: set[str]) -> tuple[list[dict], list[dict]]:
    """Return (evidence, security_flags). Suspicious sentences are never turned into evidence."""
    clean, flagged = scan(text)
    ev: list[dict] = []
    for sent in clean:
        for topic, pat in RULES:
            if topic in allowed and re.search(pat, sent, re.I):
                ev.append(Evidence(claim=sent, source=source, source_id=source_id, date=date,
                                   confidence=confidence, topic=topic).model_dump())
        if PRICE_WORDS.search(sent):
            for amt in parse_amounts(sent):
                ev.append(Evidence(claim=sent, source=source, source_id=source_id, date=date,
                                   confidence=confidence, topic="deal_value", value=amt).model_dump())
    flags = [Evidence(claim=f"Suspicious instruction-like text ignored: \"{s[:120]}\"", source=source,
                      source_id=source_id, date=date, confidence=0.9,
                      topic="security_flag").model_dump() for s in flagged]
    return ev, flags
