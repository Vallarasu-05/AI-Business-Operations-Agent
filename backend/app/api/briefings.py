from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from app.security.auth import require_api_key
from app.services import execution_service as svc

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.get("/{execution_id}")
def briefing(execution_id: str):
    ex = svc.EXECUTIONS.get(execution_id)
    if not ex or not ex["state"].get("briefing"):
        raise HTTPException(404, "No briefing for this execution")
    return {"briefing": ex["state"]["briefing"], "quality": ex["state"].get("quality")}


@router.get("/{execution_id}/markdown", response_class=PlainTextResponse)
def markdown(execution_id: str):
    ex = svc.EXECUTIONS.get(execution_id)
    if not ex or not ex["state"].get("briefing_markdown"):
        raise HTTPException(404, "No briefing for this execution")
    return ex["state"]["briefing_markdown"]


@router.get("/{execution_id}/pdf")
def pdf(execution_id: str):
    ex = svc.EXECUTIONS.get(execution_id)
    path = ((ex or {}).get("state", {}).get("delivery") or {}).get("pdf")
    if not path:
        raise HTTPException(404, "PDF is generated after approval/delivery")
    return FileResponse(path, media_type="application/pdf", filename=f"{execution_id}.pdf")
