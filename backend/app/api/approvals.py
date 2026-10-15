from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.security.auth import require_api_key
from app.services import execution_service as svc

router = APIRouter(dependencies=[Depends(require_api_key)])


class Decision(BaseModel):
    status: Literal["approved", "edited", "rejected"]
    email_body: str | None = None


@router.post("/{execution_id}")
def decide(execution_id: str, body: Decision):
    if execution_id not in svc.EXECUTIONS:
        raise HTTPException(404, "Unknown execution")
    try:
        svc.resume(execution_id, body.model_dump())
    except ValueError as e:
        raise HTTPException(409, str(e))
    return {"ok": True}
