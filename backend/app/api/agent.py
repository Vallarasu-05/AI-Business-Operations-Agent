from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.security.auth import require_api_key
from app.services import execution_service

router = APIRouter(dependencies=[Depends(require_api_key)])


class RunRequest(BaseModel):
    request: str


@router.post("/run")
def run_agent(body: RunRequest):
    return {"execution_id": execution_service.start_run(body.request)}
