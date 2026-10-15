import re

AMOUNT_RE = re.compile(
    r"(?:₹|Rs\.?|INR)\s?([\d,]+(?:\.\d+)?)\s*(crores?|cr|lakhs?|lacs?|l)?\b", re.I
)
_MULT = {"crore": 1e7, "crores": 1e7, "cr": 1e7, "lakh": 1e5, "lakhs": 1e5,
         "lac": 1e5, "lacs": 1e5, "l": 1e5}


def parse_amounts(text: str) -> list[float]:
    out = []
    for m in AMOUNT_RE.finditer(text or ""):
        num = m.group(1).replace(",", "")
        if not num or num == ".":
            continue
        out.append(float(num) * _MULT.get((m.group(2) or "").lower(), 1))
    return out


def fmt_inr(v: float) -> str:
    n = int(round(v))
    s = str(n)
    if len(s) <= 3:
        return "₹" + s
    last3, rest, parts = s[-3:], s[:-3], []
    while len(rest) > 2:
        parts.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        parts.insert(0, rest)
    return "₹" + ",".join(parts + [last3])
