from pathlib import Path
from langchain_core.runnables import RunnableConfig
from app.config import settings
from app.memory import customer_memory
from app.services import notification_service, pdf_service


def deliver(state, config: RunnableConfig):
    """READ -> REASON -> DRAFT -> APPROVE -> WRITE. The email only goes out if a human approved it."""
    run_id = config["configurable"]["thread_id"]
    out = Path(settings.output_dir) / "briefings"
    out.mkdir(parents=True, exist_ok=True)
    md_path, pdf_path = out / f"{run_id}.md", out / f"{run_id}.pdf"
    md_path.write_text(state["briefing_markdown"], encoding="utf-8")
    pdf_service.markdown_to_pdf(state["briefing_markdown"], str(pdf_path))
    result = {"markdown": str(md_path), "pdf": str(pdf_path)}

    if state.get("approval_status") in ("approved", "edited"):
        d = state["email_draft"]
        result["email"] = notification_service.send_email(d["to"], d["subject"], d["body"], str(pdf_path))
        customer_memory.update_from_briefing(state["customer"].get("company_id"), state["briefing"])
    else:
        result["email"] = {"status": "skipped", "reason": "rejected by reviewer"}
    return {"delivery": result}
