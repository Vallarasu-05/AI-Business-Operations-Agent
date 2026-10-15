"""Runs the LangGraph agent in background threads and tracks step-by-step progress for the UI."""
import logging
import threading
import time
import uuid
from datetime import datetime

from langgraph.types import Command

from app.agent.graph import NODE_ORDER, build_graph
from app.memory.checkpointer import get_checkpointer

log = logging.getLogger(__name__)
EXECUTIONS: dict[str, dict] = {}
_graph = None
_lock = threading.Lock()


def graph():
    global _graph
    with _lock:
        if _graph is None:
            _graph = build_graph(get_checkpointer())
    return _graph


def _detail(upd: dict) -> str:
    bits = [f"{k}: {len(v)}" for k, v in upd.items() if isinstance(v, (list, dict)) and v and
            k in ("evidence", "errors", "conflicts", "risks", "recommended_topics", "meetings")]
    return ", ".join(bits)


def _interrupt_payload(snap):
    for t in snap.tasks:
        if t.interrupts:
            return t.interrupts[0].value
    return None


def _drive(eid: str, payload) -> None:
    ex, cfg = EXECUTIONS[eid], {"configurable": {"thread_id": eid}}
    ex["status"] = "running"
    try:
        for chunk in graph().stream(payload, cfg, stream_mode="updates"):
            for node, upd in chunk.items():
                if node.startswith("__"):
                    continue
                ex["steps"].append({"node": node, "status": "success", "at": time.time(),
                                    "detail": _detail(upd or {})})
        snap = graph().get_state(cfg)
        ex["state"] = snap.values
        if snap.next:
            ex["status"], ex["interrupt"] = "waiting_approval", _interrupt_payload(snap)
        else:
            ex["status"], ex["interrupt"] = "completed", None
    except Exception as e:  # noqa: BLE001
        log.exception("run %s failed", eid)
        ex["status"], ex["error"] = "failed", str(e)
    finally:
        _persist(ex)


def _persist(ex: dict) -> None:
    try:
        from app.db.models import AgentRun
        from app.db.session import SessionLocal, init_db
        init_db()
        st = ex.get("state") or {}
        with SessionLocal() as s:
            s.merge(AgentRun(id=ex["id"], request=ex["request"], status=ex["status"], steps=ex["steps"],
                             briefing=st.get("briefing"), quality=st.get("quality"),
                             finished_at=datetime.utcnow() if ex["status"] in ("completed", "failed") else None))
            s.commit()
    except Exception:  # noqa: BLE001  (persistence must never break a run)
        log.exception("could not persist run")


def start_run(request: str) -> str:
    eid = "run_" + uuid.uuid4().hex[:10]
    EXECUTIONS[eid] = {"id": eid, "request": request, "status": "queued", "steps": [], "state": {},
                       "interrupt": None, "error": None, "created": time.time()}
    threading.Thread(target=_drive, args=(eid, {"user_request": request}), daemon=True).start()
    return eid


def resume(eid: str, decision: dict) -> None:
    ex = EXECUTIONS[eid]
    if ex["status"] != "waiting_approval":
        raise ValueError("Execution is not waiting for approval")
    ex["status"] = "running"
    threading.Thread(target=_drive, args=(eid, Command(resume=decision)), daemon=True).start()


def view(eid: str) -> dict | None:
    ex = EXECUTIONS.get(eid)
    if not ex:
        return None
    return {**ex, "steps_order": NODE_ORDER}
