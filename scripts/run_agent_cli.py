"""Run the agent in the terminal (auto-approves).  python ../scripts/run_agent_cli.py "Prepare tomorrow's sales meeting with ABC Corporation" """
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from langgraph.types import Command  # noqa: E402
from app.agent.graph import build_graph  # noqa: E402

req = sys.argv[1] if len(sys.argv) > 1 else "Prepare tomorrow's sales meeting with ABC Corporation"
g = build_graph()
cfg = {"configurable": {"thread_id": uuid.uuid4().hex}}
for chunk in g.stream({"user_request": req}, cfg, stream_mode="updates"):
    for node in chunk:
        if not node.startswith("__"):
            print("✓", node)
state = g.get_state(cfg).values
print("\n" + state["briefing_markdown"])
print("\nQuality:", state["quality"])
if input("\nApprove & 'send' email? [y/N] ").lower() == "y":
    g.invoke(Command(resume={"status": "approved"}), cfg)
    print(g.get_state(cfg).values["delivery"])
