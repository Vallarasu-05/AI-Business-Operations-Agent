from app.services.money import fmt_inr


def _cite(ids: list[str]) -> str:
    return " " + "".join(f"[{i}]" for i in ids) if ids else ""


def _items(lines: list[dict], empty: str = "None identified.") -> str:
    return "\n".join(f"- {i['text']}{_cite(i.get('evidence_ids', []))}" for i in lines) or empty


def render_markdown(b: dict) -> str:
    m, deal = b["meeting"], b.get("deal") or {}
    out = [f"# {b['customer']['name']} - Sales Meeting Brief", "",
           f"**Meeting:** {m['title']}  ", f"**When:** {m['date']}, {m['start']} - {m['end']}  ",
           f"**Participants:** {', '.join(a['name'] for a in m['attendees'])}", "",
           "## Executive Summary", b["executive_summary"], ""]
    if deal:
        out += ["## Deal", f"- {deal['name']}: {fmt_inr(deal['value'])}, stage **{deal['stage']}**, "
                f"expected close {deal.get('close_date', 'n/a')}" + _cite(deal.get("evidence_ids", [])), ""]
    c = b["customer"]
    out += ["## Customer", f"- Industry: {c.get('industry', 'n/a')}",
            f"- Matched via: {c.get('matched_via', '')} (confidence {c.get('confidence', 0):.2f})", ""]
    mem = b.get("memory") or {}
    if mem.get("known_concerns"):
        out += ["## Customer Memory (previous meetings)",
                *[f"- Known concern: {x}" for x in mem["known_concerns"]], ""]
    out += ["## Previous Discussions", _items(b["previous_discussions"]), "",
            "## Open Issues", _items(b["open_issues"]), "",
            "## Customer Concerns", _items(b["objections"]), "",
            "## Pending Decisions", _items(b["pending_decisions"]), "",
            "## Risks"]
    out += [f"- **{r['severity'].upper()}** - {r['risk']}: {r['rationale']}{_cite(r['evidence_ids'])}"
            for r in b["risks"]] or ["None identified."]
    out += ["", "## Data Conflicts"]
    out += [f"- **{c['topic']}**: " + " vs ".join(f"{g['display']} ({', '.join(g['sources'])}){_cite(g['evidence_ids'][:2])}"
            for g in c["groups"]) + f". {c['note']}" for c in b["conflicts"]] or ["None detected."]
    out += ["", "## Opportunities", _items(b["opportunities"]), "", "## Recommended Discussion"]
    for i, t in enumerate(b["recommended_topics"], 1):
        out += [f"{i}. **{t['topic']}** - {t['why']}{_cite(t['evidence_ids'])}",
                f"   - Suggested question: \"{t['suggested_question']}\""]
    out += ["", "## Sources"]
    for src, ids in b["sources"].items():
        out.append(f"- {src} ({'external' if src == 'web_search' else 'internal'}): {len(ids)} items")
    return "\n".join(out)
