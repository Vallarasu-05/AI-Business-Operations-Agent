import re

PATTERNS = [
    r"ignore (all |any )?(the )?(previous|prior|above) (instructions|prompts?)",
    r"disregard (all |any )?(previous|prior|above)",
    r"you are now",
    r"system prompt",
    r"(send|forward|email|export) (the |all )?(customer|user|contact)s?'? ?(database|data|list)",
    r"reveal (your|the) (instructions|prompt|api key|secrets?)",
]
_RE = [re.compile(p, re.I) for p in PATTERNS]


def is_suspicious(sentence: str) -> bool:
    return any(r.search(sentence) for r in _RE)


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]


def scan(text: str) -> tuple[list[str], list[str]]:
    """Return (clean_sentences, flagged_sentences)."""
    clean, flagged = [], []
    for s in split_sentences(text):
        (flagged if is_suspicious(s) else clean).append(s)
    return clean, flagged
