from fastapi import APIRouter, Depends, HTTPException
from app.security.auth import require_api_key
from app.services import execution_service as svc

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.get("")
def list_executions():
    return [{"id": e["id"], "request": e["request"], "status": e["status"], "created": e["created"]}
            for e in sorted(svc.EXECUTIONS.values(), key=lambda x: -x["created"])]


@router.get("/{execution_id}")
def get_execution(execution_id: str):
    v = svc.view(execution_id)
    if not v:
        raise HTTPException(404, "Unknown execution")
    return v
