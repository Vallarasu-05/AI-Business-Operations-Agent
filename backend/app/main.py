from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import agent, approvals, briefings, executions, meetings
from app.config import settings
from app.logging_config import setup_logging

setup_logging()
app = FastAPI(title="AI Business Operations Agent")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(agent.router, prefix="/api/agent", tags=["agent"])
app.include_router(executions.router, prefix="/api/executions", tags=["executions"])
app.include_router(approvals.router, prefix="/api/approval", tags=["approval"])
app.include_router(meetings.router, prefix="/api/meetings", tags=["meetings"])
app.include_router(briefings.router, prefix="/api/briefings", tags=["briefings"])


@app.get("/health")
def health():
    return {"status": "ok", "data_mode": settings.data_mode, "llm": bool(settings.llm_api_key)}
